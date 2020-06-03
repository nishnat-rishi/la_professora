# Kitchensink class

import random
import string
import sys

IP = 'localhost'
PORT = 1224

PROF_PORT = 1224
MINT_PORT = 1225

HLEN = 20 # FIXED!!!

DGRAM_SIZE = 4 # 0 - 4
MSG_SIZE = 8 # 4 - 8
SENDER_NAME = HLEN # 8 - 20

DGRAM_BYTES = 128

seed_value = 1244

PADDING = 10

######################### Encryptor & Decryptor ###############################



def encrypt(message):
  key = len(message)
  r_u = ord('Z') - ord('A')
  r_l = ord('z') - ord('a')
  new_str = ''
  for character in message:
    if character in string.ascii_letters:
      if ord(character) <= ord('z') and ord(character) >= ord('a'):
        new_c = chr(((ord(character) - ord('a')) + key) % r_l + ord('a'))
        new_str += new_c
      elif ord(character) <= ord('Z') and ord(character) >= ord('A'):
        new_c = chr(((ord(character) - ord('A')) + key) % r_u + ord('A'))
        new_str += new_c
    else:
      new_str += character
  return new_str

def decrypt(message, key):
  r_u = ord('Z') - ord('A')
  r_l = ord('z') - ord('a')
  new_str = ''
  for character in message:
    if character in string.ascii_letters:
      if ord(character) <= ord('z') and ord(character) >= ord('a'):
        new_c = chr(((ord(character) - ord('a')) - key) % r_l + ord('a'))
        new_str += new_c
      elif ord(character) <= ord('Z') and ord(character) >= ord('A'):
        new_c = chr(((ord(character) - ord('A')) - key) % r_u + ord('A'))
        new_str += new_c
    else:
      new_str += character
  return new_str



######################### Header & Serialization ###############################



def parse_header(header):
  '''
  HEADER_FORMAT (fixed length! no options!): 
    DATAGRAM_SIZE(4 bytes)
    MESSAGE_SIZE(4 bytes)
    CLIENT_NAME(12 bytes)
    MESSAGE(MESSAGE_SIZE bytes for TCP, DATAGRAM_SIZE - HEADER_SIZE for UDP)
  '''

  datagram_size_bytes = header[:DGRAM_SIZE]
  message_size_bytes = header[DGRAM_SIZE:MSG_SIZE]
  client_name_bytes = header[MSG_SIZE:SENDER_NAME]

  datagram_size = int(datagram_size_bytes.decode("utf-8"))
  message_size = int(message_size_bytes.decode("utf-8"))
  client_name = client_name_bytes.decode("utf-8").strip()

  return datagram_size, message_size, client_name

def serialize_with_header(message, client_name):
  datagram_size = HLEN + len(message)
  message_size = len(message.strip())
  return f"{datagram_size:<{DGRAM_SIZE}}{message_size:<{MSG_SIZE-DGRAM_SIZE}}{client_name:<{SENDER_NAME-MSG_SIZE}}{message}"

############### Incoming / Outgoing Message Handling (RELIABLE) ###############



def handle_incoming_messages_reliably(sock, receiver_name):
  while True:
    header = sock.recv(HLEN)
    datagram_size, message_size, sender_name = parse_header(header)
    if message_size <= 0:
      print(f"({sender_name} disconnected)")
      sock.close()
      break
    msg = sock.recv(message_size)
    decoded_msg = msg.decode("utf-8")
    sys.stdout.write('\010' * 128) # backspace to clear the line!
    print(f"{sender_name:>{PADDING}}: {decoded_msg}\n{receiver_name:>{PADDING}}> ", end='')

def handle_outgoing_messages_reliably(sock, sender_name):
  while True:
    sys.stdout.write('\010' * 128)
    sys.stdout.write(f"{sender_name:>{PADDING}}> ")
    message = input()
    if message == '--signout':
      break
    sock.send(bytes(serialize_with_header(message, sender_name), "utf-8"))



############### Incoming / Outgoing Message Handling (UNRELIABLE) ################



def handle_incoming_messages_unreliably(sock, receiver_name):
  while True:
    dgram, address = sock.recvfrom(DGRAM_BYTES)
    datagram_size, message_size, sender_name = parse_header(dgram[:HLEN])
    if message_size <= 0:
      print(f"({sender_name} disconnected)")
      sock.close()
      break
    msg = dgram[HLEN:]
    decoded_msg = decrypt(msg.decode("utf-8").strip(), message_size)
    sys.stdout.write('\010' * 128)
    print(f"{sender_name:>{PADDING}}: {decoded_msg}\n{receiver_name:>{PADDING}}> ", end='')

def handle_outgoing_messages_unreliably(sock, sender_name, sender_port):
  while True:
    sys.stdout.write('\010' * 128)
    sys.stdout.write(f"{sender_name:>{PADDING}}> ")
    message = input()
    if message == '--signout':
      break
    else:
      message = encrypt(message)
      message = message.ljust(DGRAM_BYTES-HLEN)
    sock.sendto(bytes(serialize_with_header(message, sender_name), "utf-8"), (IP, sender_port))


import socket
import threading
import sys
import os

import utilities as u

print("Communicate with: \n\n1 -> Raquel\n2 -> Royal Mint\n")
selection = input("(1/2)> ")
if selection.strip() == "1":
  print("\nBeginning conversation with Raquel...\n")
  os.system("start python reliable_server.py")
  os.system("start python raquel.py")
  reliable_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  reliable_server.connect(("localhost", 1224))
  sender = threading.Thread(target=u.handle_outgoing_messages_reliably, args=(reliable_server, "Professor"))
  sender.start()
  u.handle_incoming_messages_reliably(reliable_server, "Professor")
else:
  print("\nBeginning conversation with Royal Mint...\n")
  os.system("start python royal_mint.py")
  unreliable_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  unreliable_socket.bind((u.IP, u.PROF_PORT))
  sender = threading.Thread(
    target=u.handle_outgoing_messages_unreliably, 
    args=(unreliable_socket, "Professor", u.MINT_PORT)
  )
  sender.start()
  u.handle_incoming_messages_unreliably(unreliable_socket, "Professor")
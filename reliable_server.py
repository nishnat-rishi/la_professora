import socket
import threading

import utilities as u

def handle_2_way_comm(sock1, sock2):
  while True:
    header = sock1.recv(u.HLEN)
    datagram_size, message_size, client_name = u.parse_header(header)
    if message_size <= 0:
      print(f"({client_name} disconnected)")
      sock2.close()
      break
    msg = sock1.recv(message_size)
    sock2.send(header+msg)

######################################################################

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((u.IP, u.PORT))
s.listen(5)

clients = []

while True:
  print(f"Waiting for {2 - len(clients)} client{'s' if len(clients)!=1 else ''} ...")
  clientsocket, address = s.accept()
  clients.append(clientsocket)
  if len(clients) == 2:
    break

print('Both parties successfully connected!')

t1 = threading.Thread(target = handle_2_way_comm, args = (clients[0], clients[1]))
t2 = threading.Thread(target = handle_2_way_comm, args = (clients[1], clients[0]))

t1.start(), t2.start()

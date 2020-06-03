import socket
import threading

import utilities as u

##########################################################

unreliable_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

unreliable_socket.bind((u.IP, u.MINT_PORT))

sender = threading.Thread(target=u.handle_incoming_messages_unreliably, args=(unreliable_socket, "Royal Mint"))
sender.start()

u.handle_outgoing_messages_unreliably(unreliable_socket, "Royal Mint", u.PROF_PORT)

unreliable_socket.close()
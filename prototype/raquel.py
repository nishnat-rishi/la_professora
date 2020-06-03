import socket
import threading

import utilities as u

##########################################################

reliable_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
reliable_server.connect((u.IP, u.PORT))

sender = threading.Thread(target=u.handle_incoming_messages_reliably, args=(reliable_server, "Raquel"))
sender.start()

u.handle_outgoing_messages_reliably(reliable_server, "Raquel")

reliable_server.close()
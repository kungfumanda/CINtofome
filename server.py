from socket import *
from rdt.rdt import *

RDTSocket = RDT(True)

# Receive
msg = RDTSocket.receive()

file = open("received_server.txt", "wb")
file.write(msg)
print("File available!")
file.close()

# Send 
file = open("server_test.txt", "rb")
msg = file.read(RDTSocket.bufferSize)

while msg:
    RDTSocket.send_pkg(msg)
    msg = file.read(RDTSocket.bufferSize)

file.close()
RDTSocket.close_connection()
from rdt import *
from socket import *

# Send
RDTSocket = RDT()

file = open("test_file.txt","rb")
msg = file.read(RDTSocket.bufferSize)

print("Sending to host...")

while msg:
    RDTSocket.send_pkg(msg)
    msg = file.read(RDTSocket.bufferSize)

file.close()


# Receive
file = open("received_file.txt", "wb")

msg = RDTSocket.receive()
print("receiving...")

file.write(msg)
file.close()

RDTSocket.close_connection()
from socket import *

''' checar porta e endereço'''

HOST = ''
PORT = 5000 

udp_server = socket(AF_INET, SOCK_DGRAM)
client_address = (HOST, PORT)
udp_server.bind(client_address)

print("UDP Server is ready!")

msg = "teste"

file = open("recieved_server.txt", "wb")
msg, address = udp_server.recvfrom(1024) # recebe do cliente
print("Recieving...")

try:
    while msg:
        udp_server.settimeout(2)
        file.write(msg)
        msg,address = udp_server.recvfrom(1024)
except timeout:
    print("File available!")
    file.close()

file = open("server_test.txt", "rb")
msg = file.read(1024)

while msg:
    if(udp_server.sendto(msg, address)): #envia pro cliente
        print("Sending to client...")
        msg = file.read(1024)

file.close()
udp_server.close()
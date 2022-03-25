from socket import *

''' checar porta e endereço'''

HOST = ''
PORT = 5000 

udp_server = socket(AF_INET, SOCK_DGRAM)
server_adress = (HOST, PORT)
udp_server.bind(server_adress)

print("Server UDP está pronto e ouvindo!")

msg = "teste"

''' fazer a parte dos arquivos aqui também '''

while True:
    msg_rec, client_address = udp_server.recvfrom(1024) # recebe do cliente
    print(f"Message recieved: {msg_rec}\n From client: {client_address}") 
    udp_server.sendto(msg, client_address) # envia para o cliente
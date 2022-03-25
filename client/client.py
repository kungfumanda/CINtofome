from socket import *

''' checar porta e endereço'''

HOST = '127.0.0.1' 
PORT = 5000  

udp_client = socket(AF_INET, SOCK_DGRAM)
server_adress = (HOST, PORT)

'''inserir ainda leitura de arquivo teste ao invés de mensagem'''

msg = "teste"

while msg:
    udp_client.sendto(msg, server_adress)
    msg = ""

'''inserir escrita de arquivo teste ao invés de mensagem'''

msg_rec, address = udp_client.recvfrom(1024)
print(f"Message recieved: {msg_rec}\n From: {address}")

udp_client.close()
from socket import *

''' checar porta e endereço'''

HOST = '127.0.0.1' 
PORT = 5000  

udp_client = socket(AF_INET, SOCK_DGRAM)
server_address = (HOST, PORT)

'''inserir ainda leitura de arquivo teste ao invés de mensagem'''

file = open("test_file.txt","rb")
msg = file.read(1024)

while msg:
    if(udp_client.sendto(msg, server_address)):
        print("Sending to host...")
        msg = file.read(1024)

file.close()

'''inserir escrita de arquivo teste ao invés de mensagem'''

file = open("recieved_file.txt", "wb")

msg,address = udp_client.recvfrom(1024)
print("Recieving...")

try:
    while msg:
        udp_client.settimeout(2)
        file.write(msg)
        msg,address = udp_client.recvfrom(1024)
except timeout:
    udp_client.close()
    file.close()
    print ("File available!")
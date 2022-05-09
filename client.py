from socket import *
from rdt import *

#intancia um objeto do tipo RDT como um cliente
RDTSocket = RDT()

#mensagem vazia para o primeiro contato com o servidor
msg = " "

#loop de repostas para o servidor 
while True:
  
  RDTSocket.send_pkg(msg.encode())

  resp = RDTSocket.receive()

  #se o cliente receber uma resposta de "ok" do server, encerra a conexão
  if (resp.decode('utf-8') == "ok"):
    break

  msg = input(resp.decode('utf8'))


resp = RDTSocket.receive()
print(resp.decode())

RDTSocket.close_connection()
    
    
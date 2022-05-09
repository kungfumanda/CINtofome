from cgi import print_arguments, print_form
from hashlib import new
from socket import *
from rdt import *
from datetime import *

#Definindo os comandos do cliente
options = "1 - cardápio\n2 - pedir \n3 - conta individual\n4 - conta da mesa\n5 - pagar\n6 - levantar"
new_line = '\n'

def horario():
  relogio = datetime.now()
  return relogio.strftime("%X")[:5]

#define o cardapio
cardapio =  {
  1: ('pao com mortadela', '2.00'),
  2: ('qualquer coisa vegana', '40.00'),
  3: ('prato do dia', '3.00'),
  4: ('arroz com feijao', '4.00')
}

#cria um objeto vazio de pedidos
pedidos = {}

#funcao que constroi o cardapio a ser exibido
def showCardapio():
  card = ""
  for x, y in cardapio.items():
    card = card + " " + str(x) + " " + str(y[0]) + " " + " " + str(y[1]) + "\n" 
  return card

#Funcao que preenche o objeto "pedidos" com o pedido de um cliente de uma mesa
def pedido(mesa, cliente, data):
  
  #pega o item do cardapio que foi pedido
  prato = cardapio.get(int(data.decode()))

  #adiciona o pedido,e atualiza o valor na conta da mesa e do cliente
  pedidos[mesa][cliente]["pedidos"].append(prato)
  pedidos[mesa]["total"] += float(prato[1])
  pedidos[mesa][cliente]["comanda"] += float(prato[1])

#retorna a lista dos pedidos de determinado cliente, e o valor total da conta
def pedir_conta(mesa, cliente):
  conta = f"{new_line}"
  valor = pedidos[mesa][cliente]["comanda"]

  for produto in pedidos[mesa][cliente]["pedidos"]:
    conta += f"{produto[0]} -> {str(produto[1])} {new_line}"
  
  return conta,valor

#instancia um objeto do tipo RDT (1 para indicar que eh um server)
RDTSocket = RDT(1)
data = RDTSocket.receive()

#envia ao cliente uma mensagem básica e espera o retorno de um "chefia"
data = horario() + " cliente: "
RDTSocket.send_pkg(data.encode())
data = RDTSocket.receive()

#enquanto não receber um chefia, vai continuar mandando a mesma mensagem até receber
while(data.decode() != "chefia"):
  data = horario() + " cliente:"
  RDTSocket.send_pkg(data.encode())
  data = RDTSocket.receive()

#manda uma requisição de mesa para o cliente, e espera a resposta
data = horario() + " CINtofome: Digite Sua mesa\n" + horario() + " cliente: "
RDTSocket.send_pkg(data.encode())
data = RDTSocket.receive()
mesa = data.decode()

#manda uma requisição de nome pro cliente, e espera a resposta
data = horario() + " CINtofome: Digite Seu nome: \n" + horario() + " cliente: "
RDTSocket.send_pkg(data.encode())
data = RDTSocket.receive()
nome = data.decode()

#recebe a tupla contendo o endereco de IP e porta do cliente que esta em contato
ipPorta = RDTSocket.sender_addr

# Atualiza tabela geral para inserir a mesa
if mesa not in pedidos:
  pedidos[mesa] = {
    "total": 0.0 
    }

# Insere cliente
pedidos[mesa].update({
  nome: {
      "nome": nome, 
      "comanda": 0.0,
      "socket": ipPorta,
      "pedidos": []
    }
  })

#informa os comandos disponiveis ao cliente
data = f"{horario()} CINtofome: Digite uma das opcoes a seguir (ou numero ou por extenso) {new_line}{options}{new_line}{horario()} {nome}: "
RDTSocket.send_pkg(data.encode())

pagamento = True

#depois de cadastrado entrara num loop de opcoes ate o cliente levantar (encerrar conexao)
while True:
  
  #recebe a opcao desejada
  req = RDTSocket.receive()
  data = req.decode('utf8')

  # se for 1, ou "cardapio", exibe o cardapio
  if (data == "1" or data == "cardápio"):
    resp = horario() + " CINtofome:\n" + showCardapio() + horario() +" " + nome + ": "

  # se for 2, ou "pedir", faz um pedido
  if (data == "2" or data == "pedir"):
    resp = horario() + " CINtofome: Digite o primeiro item que gostaria (número) \n" + horario() +" " + nome +": "
    RDTSocket.send_pkg(resp.encode())
    
    data = RDTSocket.receive()
    # continua perguntando por pedidos ate o cliente dizer nao
    while True:
      pedido(mesa,nome,data)
    
      resp = horario() + " CINtofome : Gostaria de mais algum item? (número ou por extenso) \n" + horario() +" " + nome + ": "
      RDTSocket.send_pkg(resp.encode())
      data = RDTSocket.receive() 

      if(str(data.decode()) == "nao"):
        break
    resp = horario() + " CINtofome: É pra já! \n" + horario() +" " + nome + ": "
    
    pagamento = False
  
  #se for 3, ou "conta individual", exibe a conta do cliente que esta se comunicando com o servidor
  if(data == "3" or data == "conta individual"):
    conta,valor = pedir_conta(mesa,nome)

    resp = f"CINtofome: Sua conta total é:{new_line}{conta}------------- {new_line}Valor: {str(valor)}"
    resp += f"{new_line}{horario()} {nome}: "

  #se for 4, ou "conta da mesa", exibe a conta da mesa do cliente que esta se comunicando com o servidor
  if(data == "4" or data == "conta da mesa"):
    total = str(pedidos[mesa]["total"])
    resp = f"CINtofome:{new_line}"

    for cliente in pedidos[mesa]:
      if cliente != "total":
        conta,valor = pedir_conta(mesa,cliente)
        if valor > 0:
          resp += f"{new_line}{cliente}{new_line}{conta}-------------{new_line}Valor: {str(valor)}{new_line}-------------"

    resp += f"{new_line}Valor total da mesa: {total}" 
    resp += f"{new_line}{horario()} {nome}: "

  # se for 5, ou "pagar", faz o pagamento da conta
  if(data == "5" or data == "pagar"):
    comanda = pedidos[mesa][nome]["comanda"]
    total = pedidos[mesa]["total"]
    valido = False
    dif = 0

    # Repassa valores para o cliente e aguarda pagamento
    base = f"Sua conta foi {comanda} e a da mesa foi {total}. Digite o valor a ser pago. {new_line}{horario()} {nome}: "
    resp = f"{horario()} CINtofome: {base}"
    RDTSocket.send_pkg(resp.encode())
    data = RDTSocket.receive() 
    data = data.decode()
 
    while True: # Trata se o pagamento é válido, se mantém aqui até receber confirmação ou cancelamento do pagamento

      if str(data) == "nao":
        resp = f"{horario()} CINtofome: Operação de pagamento cancelada!"
        break

      if (valido and str(data) == "sim"): # Faz operações de confirmação       
        
        # Retirar os pedidos do cliente
        pedidos[mesa][nome]["comanda"] = 0.0
        pedidos[mesa][nome]["pedidos"] = []
        pedidos[mesa]["total"] -= comanda

        # Calcula e retira extra pago, se tiver
        if dif > 0: 
          pedidos[mesa]["total"] -= dif
         
          # Separa os clientes que tem comandas ativas para dividir o valor extra
          com_conta = [c for c in pedidos[mesa] if c != "total" and pedidos[mesa][c]["comanda"] > 0]
          dif_ind = dif/len(com_conta)

          for cliente in com_conta:
            pedidos[mesa][cliente]["comanda"] -= dif

        resp = f"{horario()} CINtofome: Conta paga, obrigado! {new_line}" 
        pagamento = True
        break
      
      if (float(data) > comanda) and float(data) <= total: # Se tiver inserido um valor válido 
        dif = float(data) - comanda
        resp = f"{horario()} Cintofome: Você está pagando {dif} a mais que sua conta.{new_line}{horario()} Cintofome: O valor excedente será distribuído.{new_line}{horario()} Cintofome: "
        valido = True
        RDTSocket.send_pkg(resp.encode())
      elif (float(data) == comanda): # Pagamento exato
        resp = f"{horario()} Cintofome: "
        valido = True
      elif (float(data) > total): # Se tiver inserido um valor maior do que a conta da mesa
        resp = f"{horario()} Cintofome: Valor maior do que o esperado, no momento não aceitamos gorjetas. {new_line}" + base
      elif (float(data) < comanda): # Se tiver inserido um valor menor que a conta individual
        resp = f"{horario()} Cintofome: Pagamento menor que o devido, nao fazemos fiado. {new_line}" + base
          
      if valido:
        resp += f"Deseja confirmar o pagamento? (digite sim para confirmar){new_line}{horario()} {nome}: "

      RDTSocket.send_pkg(resp.encode())
      data = RDTSocket.receive()
      data = data.decode()
      
    resp += f"{horario()} {nome}: "
  #se receber 6, ou "levantar", vai checar se houve o pagamento, se nao vai enviar uma mensagem para o cliente e reiniciar o loop 
  if((data == "6" or data == "levantar") and ~pagamento):
    resp = horario() + " " + nome + ": Você ainda não pagou sua conta\n" + horario() + " " + nome + ": "

  #se receber 6, ou "levantar", vai checar se houve o pagamento
  if((data == "6" or data == "levantar") and pagamento):
    #se houve o pagamento envia uma mensagem de ok para o cliente encerrar conexão
    resp = "ok"
    #deleta aquele cliente cadastrado
    del pedidos[mesa][nome]
    RDTSocket.send_pkg(resp.encode())
    break

  RDTSocket.send_pkg(resp.encode())

# Encerra conexao com cliente
data = horario() + " " + nome + ": Volte sempre ^^ \n"
RDTSocket.send_pkg(data.encode())

RDTSocket.close_connection()




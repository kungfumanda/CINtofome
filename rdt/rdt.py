from socket import *
from utils.checksum import checksum
import time

class RDT:

    def __init__(self, isServer = False, addressPort = ("127.0.0.1", 20001), bufferSize = 1024):
        self.isServer = isServer
        self.timer = 10.0
        self.addressPort =  addressPort
        self.bufferSize = bufferSize
        
        self.sender_addr = 0
        self.seq_num = 0
        self.UDPSocket = socket(AF_INET, SOCK_DGRAM)
        
        if isServer:
            self.UDPSocket.bind(self.addressPort)
            self.UDPSocket.settimeout(self.timer)
            print(msgs["server"]["run"])
        else:
            print(msgs["client"]["run"])
    
    def send(self, msg):
        if self.isServer:
            print(msgs["server"]["send"]) 
            self.UDPSocket.sendto(msg, self.sender_addr)
        else:
            print(msgs["client"]["send"])
            self.UDPSocket.sendto(msg, self.addressPort)

    def send_pkg(self, msg):
        msg = self.create_header(msg.decode())
        ack = False
        start =  time.process_time() # Iniciando o temporizador

        while not ack:
            self.send(msg)

            try:
                msg, self.sender_addr = self.UDPSocket.recvfrom(self.bufferSize)
            except socket.timeout:
                print(msgs["ack"]["not"])
            else:
                ack = self.rcv_ack(msg)

        self.timer = time.process_time() - start # self.timer armazenando o tempo decorrido para enviar e confirma a entrega

    def receive(self):
        print(msgs["receiv"]["going"])
        
        self.UDPSocket.settimeout(self.timer + 0.01)
        msg, self.sender_addr = self.UDPSocket.recvfrom(self.bufferSize)
        msg = self.rcv_pkg(msg)

        if msg: 
            buffer = msg
        
        print(msgs["receiv"]["done"])
        return buffer.encode()

    def send_ack(self, ack):
        if ack:
            msg = self.create_header("ACK")
        else:
            msg = self.create_header("NACK")
        
        self.send(msg)


    def rcv_pkg(self, msg):
        msg = eval(msg.decode())
        seq_num = msg['seq']
        checksum = msg['checksum']
        payload = msg['payload']

        if self._checksum(checksum, payload) and seq_num == self.seq_num:
            self.send_ack(1)
            self.seq_num = 1 - self.seq_num
            return payload
        else:
            self.send_ack(0)
            return False
    

    def rcv_ack(self, msg):
        msg = eval(msg.decode())
        seq_num = msg['seq']
        checksum = msg['checksum']
        payload = msg['payload']

        if self._checksum(checksum, payload) and seq_num == self.seq_num and payload == "ACK":
            self.seq_num = 1 - self.seq_num
            return True
        else:
            return False


    def _checksum(self, cs, payload):
        if checksum(payload) == cs:
            return True
        else:
            return False


    def create_header(self, msg):

        chcksum = checksum(msg)

        return str({
            'seq': self.seq_num,
            'checksum': chcksum,
            'payload' : msg
        }).encode()

    def close_connection(self):
        print("Closing socket")
        self.UDPSocket.close()



msgs = {
    "server": {
        "run": "Server Running!",
        "send": "Sending to Client!"
    },
    "client": {
        "run": "Client Running!",
        "send": "Sending to Server!"
    },
    "ack": {
        "not": "Did not receive ACK. Sending again."
    },
    "receiv": {
        "going": "Receiveing package",
        "done": "Received"
    }
}



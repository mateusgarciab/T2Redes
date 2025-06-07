import socket
import pickle
import copy
from baralho import *
        
class Mensagem():
    def __init__(self, tipo, origem, destino, cartaId):
        self.tipo = tipo
        self.cartaID = cartaId
        self.origem = origem
        self.destino = destino

    def imprimeMensagem(self):
        print(f"Mensagem do tipo {self.tipo}, origem {self.origem}, destino {self.destino} e carta ID {self.cartaID}")  

    def enviaMensagem(self, ipEnvio, portaEnvio):
        soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Enviado")
        self.imprimeMensagem()
        soquete.sendto(pickle.dumps(self), (ipEnvio, int(portaEnvio)))

        soquete.close()

    def mensagemParaMim(self, maquina):
        if self.destino+1 == maquina:
            return True
        else:
            return False

def recebeMensagem(ipChegada, portaChegada) -> Mensagem:
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soquete.bind((ipChegada, int(portaChegada)))
    print("Esperar")
    #recebe
    while True:
        dados, addr = soquete.recvfrom(1024) 
        mensagem = pickle.loads(dados)
        print(f"Recebido")
        mensagem.imprimeMensagem()
        soquete.close()
        return mensagem

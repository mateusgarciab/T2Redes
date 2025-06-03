import socket
import pickle
import copy
from baralho import *
        
class Mensagem():
    def __init__(self, tipo, origem, destino):
        self.tipo = tipo
        self.carta = Carta(0,0,0,0)
        self.origem = origem
        self.destino = destino

    def imprimeMensagem(self):
        print(f"Mensagem do tipo {self.tipo}")  

    def enviaMensagem(self, ipEnvio, portaEnvio):
        soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        soquete.sendto(pickle.dumps(self), (ipEnvio, int(portaEnvio)))
        print("Enviando mensagem de tipo: ", self.tipo)

        soquete.close()


def recebeMensagem(ipChegada, portaChegada) -> Mensagem:
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soquete.bind((ipChegada, int(portaChegada)))

    #recebe
    while True:
        dados, addr = soquete.recvfrom(1024) 
        mensagem = pickle.loads(dados)
        print(f"Recebido mensagem de tipo: {mensagem.tipo}")
        """ mensagem.imprimeMensagem() """
        soquete.close()
        return mensagem


import socket
import pickle
from baralho import *
        
""" 
Tipos
0 - Começo de Jogo
1 - Distribuição de Carta 
2 - Começo Mesa/Vaza
3 - Começo de Rodada
4 - Passagem de bastão
5 - Mensagem de jogo
6 - Fim de Rodada
7 - Fim da Mesa/Vaza
8 - Fim de Jogo
"""

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
        soquete.sendto(pickle.dumps(self), (ipEnvio, int(portaEnvio)))

        soquete.close()

    def mensagemParaMim(self, maquina):
        if self.destino == maquina:
            return True
        else:
            return False

def recebeMensagem(ipChegada, portaChegada) -> Mensagem:
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soquete.bind((ipChegada, int(portaChegada)))

    while True:
        dados, addr = soquete.recvfrom(1024) 
        mensagem = pickle.loads(dados)
        soquete.close()

        return mensagem

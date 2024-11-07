import socket

class Mensagem():
    def __init__(self, tipo, bloco0, bloco1, bloco2, bloco3):
        self.tipo = tipo
        self.bloco0 = bloco0
        self.bloco1 = bloco1
        self.bloco2 = bloco2
        self.bloco3 = bloco3


def enviaConfirma(ordem):
    mensagem = Mensagem(1, 0, 0, 0, 0)
    #envia
    

def confirmaPassa(ordem):
    #recebe
    if ordem == 1:
        #adiciona na 1
    elif ordem == 2:
        #adiciona na 2
    elif ordem == 3:
        #adiciona na 3
    else:
        print("Valor invalido")
    #envia

def recebeConfirma():
    #verifica todas as posições 
    #retorna se todos conectados ou não
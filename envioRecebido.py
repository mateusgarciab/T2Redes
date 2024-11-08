import socket

class Mensagem():
    def __init__(self, tipo, bloco0, bloco1, bloco2, bloco3):
        self.tipo = tipo
        self.bloco0 = bloco0
        self.bloco1 = bloco1
        self.bloco2 = bloco2
        self.bloco3 = bloco3

def enviaMensagem(mensagem, UPD_IP, UDP_PORT):
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soquete.sendto(mensagem, (UPD_IP, UDP_PORT))
    
    soquete.close()

def recebeMensagem(UPD_IP, UDP_PORT):
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soquete.bind((UPD_IP, UDP_PORT))

    #recebe
    while True:
        dados, addr = soquete.recvfrom(1024) 
        mensagem = Mensagem(dados)
        #print("received message: %s" % mensagem)
        soquete.close()
        return mensagem

def enviaConfirma(ordem, UPD_IP, UDP_PORT):
    mensagem = Mensagem(1, 0, 0, 0, 0)
    enviaMensagem(mensagem, UPD_IP, UDP_PORT)
    

def passaConfirma(ordem, UPD_IP, UDP_PORT):
    #recebe
    mensagem = recebeMensagem(UPD_IP, UDP_PORT)
    if ordem == 1:
        #adiciona na 1
        mensagem.bloco1 = 1
    elif ordem == 2:
        #adiciona na 2
        mensagem.bloco2 = 2
    elif ordem == 3:
        #adiciona na 3
        mensagem.bloco3 = 3
    else:
        print("Valor invalido")
    #envia
        enviaMensagem(mensagem, UPD_IP, UDP_PORT)

# Verifica se a mensagem passou pela rede e todos digitaram numeros diferentes de rodada
def recebeConfirma(UPD_IP, UDP_PORT):
    #verifica todas as posições 
    #retorna se todos conectados ou não
    mensagem = recebeMensagem(UPD_IP, UDP_PORT)
    if mensagem.tipo == 1 and mensagem.bloco0 == 0 and mensagem.bloco1 == 1 and mensagem.bloco2 == 2 and mensagem.bloco3 == 3:
        return True
    return False
import socket
import pickle

class Mensagem():
    def __init__(self, tipo, bloco0, bloco1, bloco2, bloco3):
        self.tipo = tipo
        self.bloco0 = bloco0
        self.bloco1 = bloco1
        self.bloco2 = bloco2
        self.bloco3 = bloco3

def enviaMensagem(mensagem, ipSaida, portaSaida):
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #soquete.sendto(str(mensagem).encode("utf-8"), (ipSaida, portaSaida))
    soquete.sendto(pickle.dumps(mensagem), (ipSaida, portaSaida))
    print("enviado ")
    
    soquete.close()

def recebeMensagem(ipChegada, portaChegada):
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soquete.bind((ipChegada, portaChegada))

    #recebe
    while True:
        dados, addr = soquete.recvfrom(1024) 
        #mensagem = Mensagem(dados.decode())
        mensagem = pickle.loads(dados)
        print("recebido ")
        print("received message: ", mensagem.tipo, " ", mensagem.bloco0, " ", mensagem.bloco1, " ", mensagem.bloco2, " ", mensagem.bloco3)
        soquete.close()
        return mensagem

def enviaConfirma(ordem, ipSaida, portaSaida):
    mensagem = Mensagem(1, 0, 0, 0, 0)
    enviaMensagem(mensagem, ipSaida, portaSaida)
    

def passaConfirma(ordem, ipChegada, portaChegada, ipSaida, portaSaida):
    #recebe
    mensagem = recebeMensagem(ipChegada, portaChegada)
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
    enviaMensagem(mensagem, ipSaida, portaSaida)

# Verifica se a mensagem passou pela rede e todos digitaram numeros diferentes de rodada
def recebeConfirma(ipChegada, portaChegada):
    #verifica todas as posições 
    #retorna se todos conectados ou não
    mensagem = recebeMensagem(ipChegada, portaChegada)
    if mensagem.tipo == 1 and mensagem.bloco0 == 0 and mensagem.bloco1 == 1 and mensagem.bloco2 == 2 and mensagem.bloco3 == 3:
        print("True ")
        return True
    
    return False
import socket
import pickle
import baralho as br

class Bloco():
    def __init__(self, carta, valorDaMao, acao, aposta):
        self.carta = carta
        self.valorDaMao = valorDaMao
        self.acao = acao
        self.aposta = aposta
        
class Mensagem():
    def __init__(self, tipo, bloco0, bloco1, bloco2, bloco3):
        self.tipo = tipo
        self.bloco0 = bloco0
        self.bloco1 = bloco1
        self.bloco2 = bloco2
        self.bloco3 = bloco3

def enviaMensagem(mensagem, ipSaida, portaSaida):
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

def passaBastao(ipChegada, portaChegada, ipSaida, portaSaida):
    mensagem = Mensagem(0, ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0)) 
    enviaMensagem(mensagem, ipSaida, portaSaida) # Passagem de bastão, tipo 0
    mensagem = recebeMensagem(ipChegada, portaChegada)
    enviaMensagem(mensagem, ipSaida, portaSaida) # Confirmação de passagem, tipo 6


def distribuiCartas(maos, mensagem, verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida):
    baralho = br.criaBaralho()
    carta = br.Carta(0,0)
    bloco = Bloco(carta, 0, 0, 0)

    if verificaJogadores[0]:
        carta = br.cartaAleatoria(baralho)
        maos[0].append(carta)
        bloco.carta = carta
        bloco.valorDaMao = br.valorMao(maos[0])
        mensagem.bloco0 = bloco

    if verificaJogadores[1]:
        carta = br.cartaAleatoria(baralho)
        maos[1].append(carta)
        bloco.carta = carta
        bloco.valorDaMao = br.valorMao(maos[1])
        mensagem.bloco1 = bloco

    if verificaJogadores[2]:
        carta = br.cartaAleatoria(baralho)
        maos[2].append(carta)
        bloco.carta = carta
        bloco.valorDaMao = br.valorMao(maos[2])
        mensagem.bloco2 = bloco

    if verificaJogadores[3]:
        carta = br.cartaAleatoria(baralho)
        maos[3].append(carta)
        bloco.carta = carta
        bloco.valorDaMao = br.valorMao(maos[3])
        mensagem.bloco3 = bloco

        mensagem.tipo = 2 # Mensagem normal de jogo
        enviaMensagem(mensagem, ipSaida, portaSaida)
        mensagem = recebeMensagem(ipChegada, portaChegada)
        return mensagem
    
def recebeAcoes(mensagem, verificaJogadores, apostas):
    if verificaJogadores[0]:
        if mensagem.bloco0.acao == 2:
            apostas[0] += 1
        elif mensagem.bloco0.acao == 3:
            verificaJogadores[0] = False

    if verificaJogadores[1]:
        if mensagem.bloco1.acao == 2:
            apostas[1] += 1
        elif mensagem.bloco1.acao == 3:
            verificaJogadores[1] = False

    if verificaJogadores[2]:
        if mensagem.bloco2.acao == 2:
            apostas[2] += 1
        elif mensagem.bloco2.acao == 3:
            verificaJogadores[2] = False

    if verificaJogadores[3]:
        if mensagem.bloco3.acao == 2:
            apostas[3] += 1
        elif mensagem.bloco3.acao == 3:
            verificaJogadores[3] = False


def verificaDesistencia(verificaJogadores, mensagem, apostas):
    if mensagem.bloco0.acao == 3:
            verificaJogadores[0] = False
            apostas[0] = 0

    if mensagem.bloco1.acao == 3:
            verificaJogadores[1] = False
            apostas[1] = 0

    if mensagem.bloco2.acao == 3:
            verificaJogadores[2] = False
            apostas[2] = 0

    if mensagem.bloco3.acao == 3:
            verificaJogadores[3] = False
            apostas[3] = 0

def quantosJogando(verificaJogadores):
    alguemVivo = verificaJogadores.count(True)
    return alguemVivo

def decideExecucao():
    decisao = int(input("Passar bastão (0) ou terminar execução (1) "))
    if decisao == 0:
        return True
    return False

def enviaFimJogo():
    Mensagem = Mensagem(4, ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0))  # Continuyar
import socket
import pickle
import baralho as br
import time

class Bloco():
    def __init__(self, carta, valorDaMao, acao, aposta):
        self.carta = carta
        self.valorDaMao = valorDaMao
        self.acao = acao
        self.aposta = aposta
        
class Mensagem():
    def __init__(self, tipo, bloco0 : Bloco, bloco1 : Bloco, bloco2 : Bloco, bloco3 : Bloco):
        self.tipo = tipo
        self.bloco0 = bloco0
        self.bloco1 = bloco1
        self.bloco2 = bloco2
        self.bloco3 = bloco3

def enviaMensagem(mensagem, ipSaida, portaSaida):
    """ time.sleep(2) """
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soquete.sendto(pickle.dumps(mensagem), (ipSaida, portaSaida))
    print("Enviando mensagem de tipo: ", mensagem.tipo)
    
    soquete.close()

def recebeMensagem(ipChegada, portaChegada):
    soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soquete.bind((ipChegada, portaChegada))

    #recebe
    while True:
        dados, addr = soquete.recvfrom(1024) 
        #mensagem = Mensagem(dados.decode())
        mensagem = pickle.loads(dados)
        print("Recebido mensagem de tipo: ", mensagem.tipo)
        soquete.close()
        return mensagem

def enviaConfirma(ordem, ipSaida, portaSaida):
    mensagem = Mensagem(1, ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0))
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

def recebeConfirma(ipChegada, portaChegada):
    mensagem = recebeMensagem(ipChegada, portaChegada)
    if mensagem.tipo == 1:
        print("True ")
        return True
    
    return False

def passaBastao(ipChegada, portaChegada, ipSaida, portaSaida):
    mensagem = Mensagem(0, ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0)) 
    enviaMensagem(mensagem, ipSaida, portaSaida) # Passagem de bastão, tipo 0
    """  mensagem = recebeMensagem(ipChegada, portaChegada)
    enviaMensagem(mensagem, ipSaida, portaSaida) # Confirmação de passagem, tipo 6 """


#Verificar essas duas

def recebeBastao(ipChegada, portaChegada, ipSaida, portaSaida):
    mensagem = Mensagem(6, ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0))
    enviaMensagem(mensagem, ipSaida, portaSaida)
    mensagem = recebeMensagem(ipChegada, portaChegada)
    enviaMensagem(mensagem, ipSaida, portaSaida)

def passaConfBastao(ipSaida, portaSaida):
    mensagem = Mensagem(6, ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0))
    enviaMensagem(mensagem, ipSaida, portaSaida)






def distribuiCartas(baralho, maos, mensagem, quemQuerMais, verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida):
    carta = br.Carta(0,0)
    bloco = Bloco(carta, 0, 0, 0)

    if verificaJogadores[0] and quemQuerMais[0]:
        carta = br.cartaAleatoria(baralho)
        maos[0].append(carta)
        bloco.carta = carta
        bloco.valorDaMao = br.valorMao(maos[0])
        mensagem.bloco0 = bloco

    if verificaJogadores[1] and quemQuerMais[1]:
        carta = br.cartaAleatoria(baralho)
        maos[1].append(carta)
        bloco.carta = carta
        bloco.valorDaMao = br.valorMao(maos[1])
        mensagem.bloco1 = bloco

    if verificaJogadores[2] and quemQuerMais[2]:
        carta = br.cartaAleatoria(baralho)
        maos[2].append(carta)
        bloco.carta = carta
        bloco.valorDaMao = br.valorMao(maos[2])
        mensagem.bloco2 = bloco

    if verificaJogadores[3] and quemQuerMais[3]:
        carta = br.cartaAleatoria(baralho)
        maos[3].append(carta)
        bloco.carta = carta
        bloco.valorDaMao = br.valorMao(maos[3])
        mensagem.bloco3 = bloco

        mensagem.tipo = 2 # Mensagem normal de jogo
        print("mandar cartas")
        enviaMensagem(mensagem, ipSaida, portaSaida)
        print("esperar")
        mensagem = recebeMensagem(ipChegada, portaChegada)
        return mensagem
    
def recebeAcoes(mensagem, quemQuerMais, verificaJogadores, apostas, fichas):
    if verificaJogadores[0]:
        if mensagem.bloco0[2] == 2:
            apostas[0] += 1
            fichas[0] -= 1
        elif mensagem.bloco0[2] == 0:
            quemQuerMais[0] = False

    if verificaJogadores[1]:
        if mensagem.bloco1[2] == 2:
            apostas[1] += 1
            fichas[1] -= 1
        elif mensagem.bloco1[2] == 0:
            quemQuerMais[1] = False

    if verificaJogadores[2]:
        if mensagem.bloco2[2] == 2:
            apostas[2] += 1
            fichas[2] -= 1
        elif mensagem.bloco2[2] == 0:
            quemQuerMais[2] = False

    if verificaJogadores[3]:
        if mensagem.bloco3[2] == 2:
            apostas[3] += 1
            fichas[3] -= 1
        elif mensagem.bloco3[2] == 0:
            quemQuerMais[3] = False

def removeEliminados(maos, quemQuerMais, verificaJogadores, apostas, fichas):
    for i in range(4):
        if verificaJogadores[i]:
            if not br.verificaMao(maos[i]):
                quemQuerMais[i] = False
                apostas[i] = 0
            if fichas[i] == 0 and apostas[i] == 0:
                verificaJogadores = False

def verificaDesistencia(quemQuerMais, mensagem : Mensagem, apostas):
    print(mensagem.bloco0[2])
    if mensagem.bloco0[2] == 3:
            quemQuerMais[0] = False
            apostas[0] = 0

    print(mensagem.bloco1[2])
    if mensagem.bloco1[2] == 3:
            quemQuerMais[1] = False
            apostas[1] = 0

    print(mensagem.bloco2[2])
    if mensagem.bloco2[2] == 3:
            quemQuerMais[2] = False
            apostas[2] = 0

    print(mensagem.bloco3[2])
    if mensagem.bloco3[2] == 3:
            quemQuerMais[3] = False
            apostas[3] = 0

def quantosJogando(verificaJogadores):
    alguemVivo = verificaJogadores.count(True)
    return alguemVivo

def decideExecucao():
    decisao = int(input("Passar bastão (0) ou terminar execução (1) "))
    if decisao == 0:
        return True
    return False

def enviaFimRodada(maos, apostas, ipChegada, portaChegada, ipSaida, portaSaida):
    mensagem = Mensagem(3, ((0,0),br.valorMao(maos[0]),0,apostas[0]), ((0,0),br.valorMao(maos[1]),0,apostas[1]), 
                        ((0,0),br.valorMao(maos[2]),0,apostas[2]), ((0,0),br.valorMao(maos[3]),0,apostas[3]))
    enviaMensagem(mensagem, ipSaida, portaSaida)
    mensagem = recebeMensagem(ipChegada, portaChegada)


def enviaFimExecucao(ipSaida, portaSaida):
    mensagem = Mensagem(5, ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0))
    enviaMensagem(mensagem, ipSaida, portaSaida)

def enviaFimJogo(verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida):
    if verificaJogadores[0] == True:
        vencedor = 0
    elif verificaJogadores[1] == True:
        vencedor = 1
    elif verificaJogadores[2] == True:
        vencedor = 2
    elif verificaJogadores[3] == True:
        vencedor = 3
    else:
        vencedor = 4 # Ninguem 
    mensagem = Mensagem(4, ((0,0),vencedor,0,0), ((0,0),vencedor,0,0), ((0,0),vencedor,0,0), ((0,0),vencedor,0,0))
    enviaMensagem(mensagem, ipSaida, portaSaida)
    mensagem = recebeMensagem(ipChegada, portaChegada)

def devolveBloco(mensagem, ordem):
    if ordem == 0:
        return mensagem.bloco0
    elif ordem == 1:
        return mensagem.bloco1
    elif ordem == 2:
        return mensagem.bloco2
    else:
        return mensagem.bloco3 

def devolveCarta(mensagem : Mensagem, ordem):
    if ordem == 0:
        bloco = mensagem.bloco0
    elif ordem == 1:
        bloco = mensagem.bloco1
    elif ordem == 2:
        bloco = mensagem.bloco2
    else:
        bloco = mensagem.bloco3
    return bloco[0]
    
def mensagemDeJogo(mensagem, acao, aposta, ordem, mao, ipSaida, portaSaida):
    carta = devolveCarta(mensagem, ordem)
    meuBloco = Bloco(carta, br.valorMao(mao), acao, aposta)
    if ordem == 0:
        mensagem.bloco0 = meuBloco
    elif ordem == 1:
        mensagem.bloco1 = meuBloco
    elif ordem == 2:
        mensagem.bloco2 = meuBloco
    elif ordem == 3:
        mensagem.bloco3 = meuBloco

    enviaMensagem(mensagem, ipSaida, portaSaida)
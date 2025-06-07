from mensagem import *
from baralho import *
from jogo import *
import info

maquina = int(input("Digite sua maquina (1 a 4) "))
valores = info.obter_valores_maquina(maquina)

ipChegada = valores[0]
ipEnvio =  valores[1]
portaChegada = valores[2]
portaEnvio =   valores[3]
"""print(f"ipChegada {ipChegada}  ipEnvio {ipEnvio}  portaChegada {portaChegada}  portaEnvio {portaEnvio}")"""

# Maquina 1 controla o jogo 
if maquina == 1:
    jogo = JogoCopas()
    for i in range(4):
        jogo.adicionar_jogador(f"Jogador {i+1}")

    print("Sou um")
    mensagem = Mensagem(0, 0, 0, 0) # Mesagem inicial para verifcar conexão
    mensagem.enviaMensagem(ipEnvio, portaEnvio)
    print("Entre envia e recebe")
    mensagem = recebeMensagem(ipChegada, portaChegada)
    jogo.distribuir_cartas(ipEnvio, portaEnvio, ipChegada, portaChegada)

    for i in range(4):
        jogo.jogadores[i].mostrar_mao()  


else: #Joga o Jogo
    print(f"Sou {maquina}")
    baralho = criaBaralho()
    jogoAtivo = True
    jogador = Jogador(f"Jogador {maquina}")

    while jogoAtivo:    
        mensagem = recebeMensagem(ipChegada, portaChegada)
        #switch case
        if mensagem.tipo == 0: # Começa jogo
            print("Tipo zero, inicio de Jogo")
            mensagem.enviaMensagem(ipEnvio, portaEnvio)
        elif mensagem.tipo == 1:
            print("Tipo 1 ")
            if mensagem.mensagemParaMim(maquina):
                print("Recebeu Carta")
                jogador.receber_carta(buscarCartaPorId(mensagem.cartaID, baralho))
                mensagem.enviaMensagem(ipEnvio, portaEnvio) # Era para mim, e repassa
            else:
                print("So passa")
                mensagem.enviaMensagem(ipEnvio, portaEnvio) # Não era para mim, e rapassa
            jogador.mostrar_mao()

        else:
            print(f"Mesagem de tipo incorreto {mensagem.tipo}")
        
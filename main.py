from mensagem import *
from baralho import *
import info
#import copy

ordem = int(input("Digite sua ordem na rodada (1 a 4) "))

valores = info.obter_valores_maquina(ordem)

ipChegada = valores[0]
ipEnvio =  valores[1]
portaChegada = valores[2]
portaEnvio =   valores[3]

# Maquina 1 controla o jogo 
if ordem == 0:
    print("Sou zero")
    mensagem = Mensagem(0, 1, 1) # Mesagem inicial para verifcar conexão
    mensagem.enviaMensagem(ipEnvio, portaEnvio)
    print("Entre envia e recebe")
    mensagem = recebeMensagem(ipChegada, portaChegada)

else: #Jogo o Jogo
    print(f"Sou {ordem}")
    mensagem = recebeMensagem(ipChegada, portaChegada)
    if mensagem.tipo == 0:
        mensagem.enviaMensagem(ipEnvio, portaEnvio)
    else:
        print(f"Mesagem de tipo incorreto {mensagem.tipo}")
        
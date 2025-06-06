from mensagem import *
from baralho import *
from jogo import *
import info
#import copy

ordem = int(input("Digite sua ordem na rodada (1 a 4) "))
valores = info.obter_valores_maquina(ordem)

ipChegada = valores[0]
ipEnvio =  valores[1]
portaChegada = valores[2]
portaEnvio =   valores[3]
jogo = JogoCopas()
for i in range(4):
    jogo.adicionar_jogador(f"Jogador {i+1}")
"""print(f"ipChegada {ipChegada}  ipEnvio {ipEnvio}  portaChegada {portaChegada}  portaEnvio {portaEnvio}")"""

# Maquina 1 controla o jogo 
if ordem == 1:
    print("Sou um")
    mensagem = Mensagem(0, 1, 1, 50) # Mesagem inicial para verifcar conexão
    mensagem.enviaMensagem(ipEnvio, portaEnvio)
    print("Entre envia e recebe")
    mensagem = recebeMensagem(ipChegada, portaChegada)

else: #Joga o Jogo
    print(f"Sou {ordem}")
    mensagem = recebeMensagem(ipChegada, portaChegada)
    if mensagem.tipo == 0:
        mensagem.enviaMensagem(ipEnvio, portaEnvio)
    else:
        print(f"Mesagem de tipo incorreto {mensagem.tipo}")
        
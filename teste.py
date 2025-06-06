import baralho as br
import random
from mensagem import *
import pickle
import info
import socket
from jogo import *
#ss -tuln
#ip a

""" jogo = JogoCopas()
for i in range(4):
    jogo.adicionar_jogador(f"Jogador {i+1}")

jogo.jogadores[0].pontosRodada = 25
jogo.jogadores[1].pontosRodada = 0
jogo.jogadores[2].pontosRodada = 1
jogo.jogadores[3].pontosRodada = 0

jogo.somaPontos()
for i in jogo.jogadores:
    print(i.pontosTotais) """

""" carta = br.Carta("ouros",2)
bloco = enre.Bloco(carta, 0, 1, 0)
mensagem = enre.Mensagem(5, bloco, enre.Bloco(br.Carta("Espada", 15), 1, 2, 3), ((0,0),0,3,0), ((0,0),0,4,0))
br.imprimeCarta(mensagem.bloco1.carta)
comprimido = pickle.dumps(mensagem)
descomprimido = pickle.loads(comprimido)
br.imprimeCarta(descomprimido.bloco1.carta) """


baralho = criaBaralho()

numero_maquina = int(input("numero da maquina "))
valores = info.obter_valores_maquina(numero_maquina)

envia = input("envia ou recebe ")

if (envia == "e"):
    msg = Mensagem(5, numero_maquina, 15, 88)
    """ comprimido = pickle.dumps(msg)
    comprimido.enviaMensagem(valores[1], valores[3]) """
    msg.enviaMensagem(valores[1], valores[3])
    msg.imprimeMensagem()


    carta = buscarCartaPorId(msg.cartaID, baralho)
    print(f"Id {msg.cartaID} {type(msg.cartaID)} {type(carta)}")
    carta.imprimeCarta()


else:
    msg = recebeMensagem(valores[0], int(valores[2]))
    """ descomprimido = pickle.loads(msg)
    descomprimido.imprimeMensagem() """


    msg.imprimeMensagem()
    carta = buscarCartaPorId(msg.cartaID, baralho)
    print(f"Id {msg.cartaID} {type(msg.cartaID)} {type(carta)}")
    carta.imprimeCarta()
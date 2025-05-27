import baralho as br
import random
import envioRecebido as enre
import pickle
import info
import socket

#ss -tuln
#ip a

""" carta = br.Carta("ouros",2)
bloco = enre.Bloco(carta, 0, 1, 0)
mensagem = enre.Mensagem(5, bloco, enre.Bloco(br.Carta("Espada", 15), 1, 2, 3), ((0,0),0,3,0), ((0,0),0,4,0))
br.imprimeCarta(mensagem.bloco1.carta)
comprimido = pickle.dumps(mensagem)
descomprimido = pickle.loads(comprimido)
br.imprimeCarta(descomprimido.bloco1.carta) """

numero_maquina = int(input("numero da maquina "))
valores = info.obter_valores_maquina(numero_maquina)

envia = input("envia ou recebe ")

if (envia == "e"):
    blocoZerado = enre.Bloco(br.Carta(0,0), 0, 0, 0)
    mensagem = enre.Mensagem(0, blocoZerado, blocoZerado, blocoZerado, blocoZerado) 
    enre.enviaMensagem(mensagem, valores[1], valores[3])
else:
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((valores[0], valores[2]))
 
    while True:
       data, addr = sock.recvfrom(1024) 
       print("received message: %s" % data)
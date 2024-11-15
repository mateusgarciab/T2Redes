import socket
import envioRecebido as enre

ipChegada = input("ip ") #"192.168.15.14" 
portaChegada = int (input("porta"))

op = int(input("chega(0) sai (1)"))

if op == 0:
    enre.recebeMensagem(ipChegada, portaChegada)
else:
    mensagem = enre.Mensagem(1, 0, 0, 0, 0)
    enre.enviaMensagem(mensagem, ipChegada, portaChegada)
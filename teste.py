import baralho as br
import random
import envioRecebido as enre

ipChegada = input("Digigite o ip de chegada ")   #"192.168.15.14"  lab4 13 10.254.225.17 
portaChegada = int(input("Digite a porta de entrada "))

ipSaida = input("Digigite o ip de saida ") 
portaSaida = int(input("Digite a porta de saida "))  

numero = int(input("Manda "))
val = int(input("val "))

if val == 1:
    mensagem = enre.Mensagem(numero, ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0)) 
    print("numero enviado", mensagem.tipo)
    enre.enviaMensagem(mensagem, ipSaida, portaSaida)

    mensagem = enre.recebeMensagem(ipChegada, portaChegada)
    print("numero recebido", mensagem.tipo)
else:
    mensagem = enre.recebeMensagem(ipChegada, portaChegada)
    print("numero recebido", mensagem.tipo)

    mensagem = enre.Mensagem(numero, ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0)) 
    print("numero enviado", mensagem.tipo)
    enre.enviaMensagem(mensagem, ipSaida, portaSaida)

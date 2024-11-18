import socket
import envioRecebido as enre
import baralho as br

ipChegada = input("Digigite o ip de chegada ")   #"192.168.15.14"  lab4 13 10.254.225.17 
portaChegada = int(input("Digite a porta de entrada "))  #5005

ipSaida = input("Digigite o ip de saida ")   #"192.168.15.14"  lab4 13 10.254.225.17 
portaSaida = int(input("Digite a porta de saida "))  #5005
mensagem = b"ola"

ordem = int(input("Digite sua ordem na rodada (0 a 3) "))

# Garante a conecção 
if ordem == 0:
    enre.enviaConfirma(ordem, ipSaida, portaSaida) 
    enre.recebeConfirma(ipChegada, portaChegada)
else:
    enre.passaConfirma(ordem, ipChegada, portaChegada, ipSaida, portaSaida)

mao_0 = []
mao_1 = []
mao_2 = []
mao_3 = []
verifica_0 = True
verifica_1 = True
verifica_2 = True
verifica_3 = True


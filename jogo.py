import socket
import envioRecebido as enre

# IP meu, do anterior ou do proximo ?
ipChegada = input("Digigite o ip de chegada ")   #"192.168.15.14"  lab4 13 10.254.225.17 
portaChegada = int(input("Digite a porta de entrada "))  #5005

ipSaida = input("Digigite o ip de saida ")   #"192.168.15.14"  lab4 13 10.254.225.17 
portaSaida = int(input("Digite a porta de saida "))  #5005
mensagem = b"ola"

ordem = int(input("Digite sua ordem na rodada (0 a 3) "))

# Garante a conecção 
if ordem == 0:
    enre.enviaConfirma(ordem, ipSaida, portaSaida) #envia confirmação
    enre.recebeConfirma(ipChegada, portaChegada)
else:
    enre.passaConfirma(ordem, ipChegada, portaChegada, ipSaida, portaSaida)


#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.sendto(mensagem, (UDP_IP, UDP_PORT))


import socket
import envioRecebido as enre

ipChegada = input("Digigite o ip de chegada ") #"192.168.15.14" # lab4 13 10.254.225.17 
portaChegada = 5005
mensagem = enre.Mensagem(1, 0, 0, 0, 0) #input("mensagem: ")

ordem = int(input("Digite sua ordem na rodada (0 a 3) "))

if ordem == 0:
    enre.enviaConfirma(ordem, ipChegada, portaChegada) #envia confirmação
    enre.recebeConfirma(ipChegada, portaChegada)
else:
    enre.passaConfirma(ordem, ipChegada, portaChegada)

#enre.enviaConfirma(ordem, ipChegada, portaChegada)
#enre.enviaMensagem(mensagem, ipChegada, portaChegada)

""" soquete = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soquete.sendto(str(mensagem).encode("utf-8"), (ipChegada, portaChegada))
    
soquete.close() """

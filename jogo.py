import socket
import envioRecebido as enre

UDP_IP = "192.168.15.14"
UDP_PORT = 5005
mensagem = b"ola"

ordem = int(input("Digite sua ordem na roda (0 a 3)"))

if ordem == 0:
    enre.enviaConfirma(ordem) #envia confirmação
    enre.recebeConfirma()
else:
    enre.confirmaPassa(ordem)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(mensagem, (UDP_IP, UDP_PORT))


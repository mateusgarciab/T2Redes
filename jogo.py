import envioRecebido as enre

# IP meu, do anterior ou do proximo ?
UDP_IP = input("Digigite o ip")   #"192.168.15.14"
UDP_PORT = 5005
mensagem = b"ola"

ordem = int(input("Digite sua ordem na rodada (0 a 3)"))

# Garante a conecção 
if ordem == 0:
    enre.enviaConfirma(ordem, UDP_IP, UDP_PORT) #envia confirmação
    enre.recebeConfirma(UDP_IP, UDP_PORT)
else:
    enre.passaConfirma(ordem, UDP_IP, UDP_PORT)


#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.sendto(mensagem, (UDP_IP, UDP_PORT))


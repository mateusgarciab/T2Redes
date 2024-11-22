import socket
import envioRecebido as enre
import baralho as br

ipChegada = input("Digigite o ip de chegada ")   #"192.168.15.14"  lab4 13 10.254.225.17 
portaChegada = int(input("Digite a porta de entrada "))

ipSaida = input("Digigite o ip de saida ")   #"192.168.15.14"  lab4 13 10.254.225.17 
portaSaida = int(input("Digite a porta de saida "))  

todosApostos = False
while not(todosApostos):
    ordem = int(input("Digite sua ordem na rodada (0 a 3) "))
    if ordem == 0:
        enre.enviaConfirma(ordem, ipSaida, portaSaida) 
        todosApostos = enre.recebeConfirma(ipChegada, portaChegada)
        if not(todosApostos):
            print("Não foi possível realizar a conexão corretamente, verifique se todos os jogadores tem uma posição diferente")
    else:
        enre.passaConfirma(ordem, ipChegada, portaChegada, ipSaida, portaSaida)

mao_0 = []
mao_1 = []
mao_2 = []
mao_3 = []
verificaJogadores = [True, True, True, True]
verificaJogo = True
bastao = False
if ordem == 0:
    bastao = True

if bastao:
    while verificaJogo:
        for i in range(4):
            if verificaJogadores[i]:
                print("teste")
        verificaJogo = False
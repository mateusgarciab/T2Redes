import envioRecebido as enre
import baralho as br

ipChegada = input("Digigite o ip de chegada ")   #"192.168.15.14"  lab4 13 10.254.225.17 
portaChegada = int(input("Digite a porta de entrada "))

ipSaida = input("Digigite o ip de saida ") 
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

mensagem = enre.Mensagem(0, ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0), ((0,0),0,0,0)) 
emExecucao = True
apostas = [0, 0, 0, 0]

bastao = False
if ordem == 0:
    bastao = True

while emExecucao:
    if bastao:
        maos = [[], [], [], []]
        verificaJogadores = [True, True, True, True]
        verificaJogadores[ordem] = False # O Dealer não joga

        mensagem = enre.distribuiCartas(maos, mensagem, verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida) 
        mensagem = enre.distribuiCartas(maos, mensagem, verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida)
        enre.verificaDesistencia(verificaJogadores, mensagem, apostas)
        
        verificaJogo = True
        while verificaJogo:
            enre.recebeAcoes(mensagem, verificaJogadores, apostas)
            quantosVivos = enre.quantosJogando(verificaJogadores)
            
            if quantosVivos == 0: # Ninguem ganhou, passa o bastão ou termina execução
                verificaJogo = False
                if enre.decideExecucao():
                    enre.passaBastao(ipChegada, portaChegada, ipSaida, portaSaida)
                else:
                    emExecucao = False

            elif quantosVivos == 1:
                verificaJogo = False
                # um jogador ganhou, passa o bastão ou termina execução, verificar isso tambem
            else:
                # segue o jogo
                mensagem = enre.distribuiCartas(maos, mensagem, verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida)
                enre.recebeAcoes(mensagem, verificaJogadores, apostas) #verificar isso aqui
    else:
        # Voce é um jogador
        fichas = 10
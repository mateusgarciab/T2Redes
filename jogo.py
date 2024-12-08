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

bastao = False
if ordem == 0:
    bastao = True

emExecucao = True
while emExecucao:
    if bastao: # Voce é o Dealer
        maos = [[], [], [], []]
        verificaJogadores = [True, True, True, True] # Responsavel pelo jogo inteiro, Jogo acaba quando no maximo um tiver True
        verificaJogadores[ordem] = False # O Dealer não joga

        while enre.quantosJogando(verificaJogadores) > 1:
            quemQuerMais = [True, True, True, True]
            quemQuerMais[ordem] = False
            baralho = br.criaBaralho()
            apostas = [1, 1, 1, 1]
            fichas = [9, 9, 9, 9]
            fichas[ordem] = 0

            mensagem = enre.distribuiCartas(baralho, maos, mensagem, quemQuerMais, verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida) 
            mensagem = enre.distribuiCartas(baralho, maos, mensagem, quemQuerMais, verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida)
            enre.verificaDesistencia(quemQuerMais, mensagem, apostas)

            verificaRodada = True
            while verificaRodada:
                enre.recebeAcoes(mensagem, quemQuerMais, verificaJogadores, apostas, fichas)
                enre.removeEliminados(maos, quemQuerMais, verificaJogadores, apostas, fichas)

                quantosVivos = enre.quantosJogando(verificaJogadores)

                # Lidar com o fim de rodada
                enre.enviaFimRodada(maos, apostas, ipChegada, portaChegada, ipSaida, portaSaida)


                if quantosVivos == 0 or quantosVivos == 1: # Fim de Jogo, passa o bastão ou termina execução
                    verificaRodada = False
                    enre.enviaFimJogo(verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida)

                    if enre.decideExecucao():
                        enre.passaBastao(ipChegada, portaChegada, ipSaida, portaSaida)
                    else:
                        emExecucao = False
                        quemQuerMais = [False, False, False, False]
                        enre.enviaFimExecucao(ipSaida, portaSaida)
                else:
                    # segue o jogo
                    mensagem = enre.distribuiCartas(baralho, maos, mensagem, quemQuerMais, verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida)

    else:
        # Voce é um jogador
        fichas = 10
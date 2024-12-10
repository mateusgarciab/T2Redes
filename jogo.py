import envioRecebido as enre
import baralho as br

ipChegada = input("Digigite o ip de chegada ")   #"192.168.15.14"  lab4 13 10.254.225.17 
portaChegada = int(input("Digite a porta de entrada "))

ipSaida = input("Digigite o ip de saida ") 
portaSaida = int(input("Digite a porta de saida "))  

ordem = int(input("Digite sua ordem na rodada (0 a 3) "))

todosApostos = False
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
                        bastao = False
                    else:
                        emExecucao = False
                        quemQuerMais = [False, False, False, False]
                        enre.enviaFimExecucao(ipSaida, portaSaida)
                else:
                    # segue o jogo
                    mensagem = enre.distribuiCartas(baralho, maos, mensagem, quemQuerMais, verificaJogadores, ipChegada, portaChegada, ipSaida, portaSaida)

    else:
        # Voce é um jogador
        jogoAtivo =True
        fichas = 9
        mao = []
        minhaAposta = 1
        while jogoAtivo:
            
            rodadaAtiva = True
            primeiraRodada = True
            podeDobra = True
            podeDesistir = True

            while rodadaAtiva:
                mensagem = enre.recebeMensagem(ipChegada, portaChegada)
                if mensagem.tipo == 0: # Recebeu o bastao
                    rodadaAtiva = False
                    bastao = True
                    enre.recebeBastao(ipChegada, portaChegada, ipSaida, portaSaida)

                elif mensagem.tipo == 2:
                    minhaCarta = enre.devolveCarta(mensagem, ordem)
                    mao.append(minhaCarta)
                    if primeiraRodada:
                        primeiraRodada = False
                    else:
                        print("Suas cartas são:")
                        br.imprimeMao(mao)
                        print("Sua aposta atual é:", minhaAposta)
                        print("Suas açoes possiveis são:")
                        print("0 - Parar")
                        print("1 - Mais uma carta")
                        if podeDobra:
                            print("2 - Dobra (Apenas uma vez por jogo)")
                        if podeDesistir:
                            print("Desistir (Apenas esssa rodada)")
                        podeDesistir = False
                        acao = int(input())
                        if acao == 2:
                            podeDobra = False
                            minhaAposta += 1
                            fichas -= 1
                        if acao == 3:
                            minhaAposta = 0
                            fichas += 1
                        enre.mensagemDeJogo(mensagem, acao, minhaAposta, ordem, mao, ipSaida, portaSaida)
                        
                elif mensagem.tipo == 3:
                    print("Fim de rodada")
                    meuBloco = enre.devolveBloco(mensagem, ordem)
                    print("Seu premio foi de", meuBloco.aposta)
                    rodadaAtiva = False
                    enre.enviaMensagem(mensagem, ipSaida, portaSaida)

                elif mensagem.tipo == 4:
                    jogoAtivo = False
                    rodadaAtiva = False
                    print("Fim de Jogo") 
                    enre.enviaMensagem(mensagem, ipSaida, portaSaida)
                    meuBloco = enre.devolveBloco(mensagem, ordem)
                    print("O vencedor foi o", meuBloco.valorDaMao)
                    #imprimir vencedor

                elif mensagem.tipo == 5:
                    emExecucao =False
                    jogoAtivo = False
                    rodadaAtiva = False
                    enre.enviaMensagem(mensagem, ipSaida, portaSaida)

                elif mensagem.tipo == 6:
                    enre.passaConfBastao(ipSaida, portaSaida)
                    print("Bastão foi passado para outro jogador")
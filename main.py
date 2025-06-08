from mensagem import *
from baralho import *
from jogo import *
import info

maquina = int(input("Digite sua maquina (1 a 4) "))
valores = info.obter_valores_maquina(maquina)

ipChegada = valores[0]
ipEnvio =  valores[1]
portaChegada = valores[2]
portaEnvio =   valores[3]
"""print(f"ipChegada {ipChegada}  ipEnvio {ipEnvio}  portaChegada {portaChegada}  portaEnvio {portaEnvio}")"""

# Maquina 1 controla o jogo 
if maquina == 1:
    jogo = JogoCopas()
    for i in range(4):
        jogo.adicionar_jogador(f"Jogador {i+1}")

    print("Sou um")
    mensagem = Mensagem(0, 1, 1, 0) # Mesagem inicial para verifcar conexão
    mensagem.enviaMensagem(ipEnvio, portaEnvio)
    print("Entre envia e recebe")
    mensagem = recebeMensagem(ipChegada, portaChegada)
    """ jogo.distribuir_cartas(ipEnvio, portaEnvio, ipChegada, portaChegada) """

    while not jogo.verificaFimJogo():
        jogo.iniciaMesa(ipEnvio, portaEnvio, ipChegada, portaChegada) #modi
            
        # Distribui cartas
        jogo.distribuir_cartas(ipEnvio, portaEnvio, ipChegada, portaChegada) #modi
        jogo.jogador_iniciante = jogo.encontraDoisCopas()
        
        # Jogo principal
        while not jogo.verificaFimMesa():
            jogo.iniciar_rodada(ipEnvio, portaEnvio, ipChegada, portaChegada) #modi

            if jogo.jogador_iniciante == 1: #Eu jogo primeiro
                idCarta = jogo.jogadores[0].jogadorJoga(jogo.cartas_na_mesa, jogo.rodada, jogo.copas_quebradas)
                #REMOVER ACARTA ADICIONAL
                del jogo.cartas_na_mesa[-1]
                jogo.jogar_rodada(0, idCarta)

                mensagem = Mensagem(5, 1, 1, idCarta)
                mensagem.enviaMensagem(ipEnvio, portaEnvio)
                mensagem = recebeMensagem(ipChegada, portaChegada)

                mensagem = Mensagem(4, 1, 2, 0)
            else:
                mensagem = Mensagem(4, 1, jogo.jogador_iniciante, 0)
            mensagem.enviaMensagem(ipEnvio, portaEnvio)

            jogo.jogadores[0].mostrar_mao()
            jogo.jogadores[1].mostrar_mao()
            jogo.jogadores[2].mostrar_mao()
            jogo.jogadores[3].mostrar_mao()
            
            while len(jogo.cartas_na_mesa) < 4: #not(mensagem.tipo == 4 and mensagem.destino == 1)
                mensagem = recebeMensagem(ipChegada, portaChegada)
                if mensagem.tipo == 5:
                    carta = buscarCartaPorId(mensagem.cartaID, jogo.baralho) # talvez o baralho já não tenha nada, se der problema pode ser aqui
                    jogo.jogar_rodada(mensagem.origem-1, mensagem.cartaID)
                    mensagem.enviaMensagem(ipEnvio, portaEnvio)
                if mensagem.tipo == 4:
                    if len(jogo.cartas_na_mesa) == 4:
                        break
                    else:
                        idCarta = jogo.jogadores[0].jogadorJoga(jogo.cartas_na_mesa, jogo.rodada, jogo.copas_quebradas)
                        jogo.jogar_rodada(0, idCarta)
                        del jogo.cartas_na_mesa[-1]
                        if len(jogo.cartas_na_mesa) != 4:
                            mensagem = Mensagem(4, maquina, (maquina%4)+1, 0)
                            mensagem.enviaMensagem(ipEnvio, portaEnvio)
                print(f"_________________ {len(jogo.cartas_na_mesa)} ____________________")
                imprimeMao(jogo.cartas_na_mesa)



            print("===========================================================================")

            """ jogo.jogar_rodada() """
            jogo.determinar_vencedor_rodada(ipEnvio, portaEnvio, ipChegada, portaChegada)

        jogo.somaPontos()
        """for i in jogo.jogadores:
            print(i.pontosRodada)"""
        for i in jogo.jogadores:
            print(i.pontosTotais)

    # Resultado final
    jogo.determinarVencedorJogo()




else: #Joga o Jogo
    baralho = criaBaralho()
    jogoAtivo = True
    jogador = Jogador(f"Jogador {maquina}")
    cartas_na_mesa = []
    copas_quebradas = False
    rodada = 0


    while jogoAtivo:    
        mensagem = recebeMensagem(ipChegada, portaChegada)
        #switch case
        if mensagem.tipo == 0: # Começa jogo
            print("Tipo zero, inicio de Jogo")
            mensagem.enviaMensagem(ipEnvio, portaEnvio)

        elif mensagem.tipo == 1:
            if mensagem.mensagemParaMim(maquina):
                print("Recebeu Carta")
                jogador.receber_carta(buscarCartaPorId(mensagem.cartaID, baralho))
                mensagem.enviaMensagem(ipEnvio, portaEnvio) # Era para mim, e repassa
            else:
                print("So passa")
                mensagem.enviaMensagem(ipEnvio, portaEnvio) # Não era para mim, e rapassa
            jogador.ordenar_mao()
            """ jogador.mostrar_mao() """

        elif mensagem.tipo == 2:
            print("===== Nova Mesa =====")
            mensagem.enviaMensagem(ipEnvio, portaEnvio) # Informa a nova Mesa, e rapassa

        elif mensagem.tipo == 3:
            rodada = mensagem.cartaID
            print(f"=== Rodada {mensagem.cartaID} ===")
            jogador.mostrar_mao()
            """if mensagem.cartaID == maquina:
                print(f"Você é o primeiro a jogar {mensagem.cartaID} ") """
            mensagem.enviaMensagem(ipEnvio, portaEnvio) # Informa a nova Rodada, e repassa

        elif mensagem.tipo == 4:
            if mensagem.destino == maquina:
                print("Você tem o bastão")
                print("Suas cartas")
                imprimeMao(jogador.mao)
                id = jogador.jogadorJoga(cartas_na_mesa, rodada, copas_quebradas)
                mensagem = Mensagem(5, maquina, maquina, id)
                mensagem.enviaMensagem(ipEnvio, portaEnvio)
                mensagem = recebeMensagem(ipChegada, portaChegada)

                print(f"_________________ {len(cartas_na_mesa)} ____________________")
                imprimeMao(cartas_na_mesa)
                if len(cartas_na_mesa) == 4:
                    mensagem = Mensagem(4, maquina, 1, 0)
                else:
                    mensagem = Mensagem(4, maquina, (maquina%4)+1, 0)
                mensagem.enviaMensagem(ipEnvio, portaEnvio)
            else:
                mensagem.enviaMensagem(ipEnvio, portaEnvio) # Bastão não é para mim

        elif mensagem.tipo == 5:
            carta = buscarCartaPorId(mensagem.cartaID, baralho)
            print(f" -- Jogador {mensagem.origem} jogou {carta.simbolo} de {carta.naipe}")
            if carta.naipe == "Copas" and not copasQuebradas:
                print("Copas foram quebradas!")
                copasQuebradas = True
            cartas_na_mesa.append(carta)
            mensagem.enviaMensagem(ipEnvio, portaEnvio)

        elif mensagem.tipo == 6:
            if mensagem.cartaID == maquina:
                print("++++++++++++ Você ganhou ++++++++++++")
            else:
                print(f"++++++++++++ {mensagem.cartaID} ganhou ++++++++++++")
            mensagem.enviaMensagem(ipEnvio, portaEnvio)
        else:
            print(f"Mesagem de tipo incorreto {mensagem.tipo}")
        
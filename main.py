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
    mensagem = Mensagem(0, 0, 0, 0) # Mesagem inicial para verifcar conexão
    mensagem.enviaMensagem(ipEnvio, portaEnvio)
    print("Entre envia e recebe")
    mensagem = recebeMensagem(ipChegada, portaChegada)
    """ jogo.distribuir_cartas(ipEnvio, portaEnvio, ipChegada, portaChegada) """

    """ for i in range(4):
        jogo.jogadores[i].mostrar_mao()   """
    while not jogo.verificaFimJogo():
        jogo.iniciaMesa(ipEnvio, portaEnvio, ipChegada, portaChegada) #modi
            
        # Distribui cartas
        jogo.distribuir_cartas(ipEnvio, portaEnvio, ipChegada, portaChegada) #modi
        
        # Jogo principal
        while not jogo.verificaFimMesa():
            jogo.iniciar_rodada(ipEnvio, portaEnvio, ipChegada, portaChegada) #modi
            jogo.jogar_rodada()
            jogo.determinar_vencedor_rodada()

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

    while jogoAtivo:    
        mensagem = recebeMensagem(ipChegada, portaChegada)
        #switch case
        if mensagem.tipo == 0: # Começa jogo
            print("Tipo zero, inicio de Jogo")
            mensagem.enviaMensagem(ipEnvio, portaEnvio)
        elif mensagem.tipo == 1:
            print("Tipo 1 ")
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
            print("=== Nova Rodada ===")
            if mensagem.cartaID == maquina:
                print(f"Você é o primeiro a jogar {mensagem.cartaID} ")
            mensagem.enviaMensagem(ipEnvio, portaEnvio) # Informa a nova Rodada, e repassa

        else:
            print(f"Mesagem de tipo incorreto {mensagem.tipo}")
        
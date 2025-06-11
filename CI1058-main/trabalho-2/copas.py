import socket
import threading
import time
import sys
import random

IP_PROPRIO = sys.argv[1]
PORTA_PROPRIA = int(sys.argv[2])
IP_PROXIMO = sys.argv[3]
PORTA_PROXIMO = int(sys.argv[4])
ID_JOGADOR = int(sys.argv[5])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_PROPRIO, PORTA_PROPRIA))

mao = []
mesa = []  # [(id_jogador, carta)]
pontuacoes = [0, 0, 0, 0]
primeira_rodada = True
copas_foram_abridas = False
mensagens_processadas = set()
token_na_mao = False
jogador_atual = None
jogadas_na_rodada = 0
round_id = 0  # NOVO: controle de rodada

naipes = ['♣', '♦', '♥', '♠']
valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
ordem = {v: i for i, v in enumerate(valores)}
baralho = [v + n for n in naipes for v in valores]

def enviar_mensagem(msg):
    sock.sendto(msg.encode(), (IP_PROXIMO, PORTA_PROXIMO))

def reenviar_mensagem(msg):
    time.sleep(0.05)
    enviar_mensagem(msg)

def distribuir_cartas():
    global baralho, round_id
    baralho = [v + n for n in naipes for v in valores]  # RESET
    random.shuffle(baralho)
    round_id += 1  # Só jogador 0 faz isso
    for i in range(4):
        mao_jogador = baralho[i*13:(i+1)*13]
        mensagem = f"CARTAS:{i}:{round_id}:{';'.join(mao_jogador)}"
        enviar_mensagem(mensagem)

def pode_jogar_carta(carta, mao_local, naipe_lider, primeira_rodada, copas_foram_abridas):
    if primeira_rodada:
        if carta[-1] == '♥' or carta == 'Q♠':
            outros_naipes = [c for c in mao_local if c[-1] != '♥' and c != 'Q♠']
            if outros_naipes:
                return False
    if not naipe_lider:
        if carta[-1] == '♥':
            if not copas_foram_abridas:
                if all(c[-1] == '♥' for c in mao_local):
                    return True
                return False
        return True
    else:
        if carta[-1] != naipe_lider:
            if any(c[-1] == naipe_lider for c in mao_local):
                return False
    return True

def processar_vaza():
    global mesa, copas_foram_abridas
    naipe_lider = mesa[0][1][-1]
    cartas_validas = [(j, c) for (j, c) in mesa if c[-1] == naipe_lider]
    vencedor = max(cartas_validas, key=lambda x: ordem[x[1][:-1]])[0]
    pontos = 0
    for _, carta in mesa:
        if carta[-1] == '♥':
            pontos += 1
            copas_foram_abridas = True
        if carta == 'Q♠':
            pontos += 13
    pontuacoes[vencedor] += pontos
    print(f"\n>>> Jogador {vencedor} ganhou a vaza! Pontos: {pontos} | Cartas: {', '.join(c for _, c in mesa)}")
    print(f"Pontuação parcial: {pontuacoes}")
    mesa.clear()
    return vencedor

def escutar():
    global token_na_mao, mao, jogador_atual, primeira_rodada, mesa, jogadas_na_rodada, pontuacoes, copas_foram_abridas, mensagens_processadas, round_id
    while True:
        data, _ = sock.recvfrom(2048)
        mensagem = data.decode()

        if mensagem in mensagens_processadas:
            continue
        mensagens_processadas.add(mensagem)

        if mensagem == "TOKEN":
            token_na_mao = True

        elif mensagem.startswith("CARTAS:"):
            partes = mensagem.split(":")
            jogador = int(partes[1])
            msg_round_id = int(partes[2])
            cartas = partes[3].split(';')

            # Atualiza round_id local sempre!
            round_id = msg_round_id

            if jogador == ID_JOGADOR:
                mao[:] = sorted(cartas, key=lambda x: (naipes.index(x[-1]), ordem[x[:-1]]))
                print(f"\nSuas cartas: {', '.join(mao)}")
                if '2♣' in mao and primeira_rodada:
                    jogador_atual = ID_JOGADOR
                    print("Você começa a rodada com 2♣!")
                    threading.Thread(target=lambda: (time.sleep(0.5), receber_token_inicial()), daemon=True).start()
            reenviar_mensagem(mensagem)

        elif mensagem.startswith("JOGADA:"):
            partes = mensagem.split(":")
            jogador = int(partes[1])
            msg_round_id = int(partes[2])
            carta = partes[3]

            # Só processa jogadas da rodada atual
            if msg_round_id != round_id:
                continue

            if all(j != jogador for (j, _) in mesa):
                mesa.append((jogador, carta))
                print(f"[JOGADOR {jogador}] jogou: {carta}")
                jogadas_na_rodada += 1
            else:
                print(f"(Ignorando jogada duplicada do jogador {jogador})")

            if len(mesa) < 4:
                jogador_atual = (jogador + 1) % 4
                reenviar_mensagem(mensagem)
                if jogador_atual == ID_JOGADOR:
                    threading.Thread(target=receber_token_inicial, daemon=True).start()
                else:
                    enviar_token()

            if len(mesa) == 4:
                vencedor = processar_vaza()
                print(f">>> Jogador {vencedor} começa a próxima vaza!\n")
                jogador_atual = vencedor
                primeira_rodada = False
                reenviar_mensagem(mensagem)
                if ID_JOGADOR == vencedor:
                    threading.Thread(target=receber_token_inicial, daemon=True).start()
                else:
                    enviar_token()

            if jogadas_na_rodada == 52:
                print("\n--- FIM DA RODADA! ---")
                print(f"Placar: {pontuacoes}")
                if max(pontuacoes) >= 100:
                    print(f"\n### FIM DE JOGO! Pontuações finais: {pontuacoes}")
                    vencedor = pontuacoes.index(min(pontuacoes))
                    print(f">>> VENCEDOR: Jogador {vencedor}")
                    print("O programa será finalizado. Parabéns!")
                    sys.exit(0)

                # Reset do estado ANTES de redistribuir cartas!
                mesa.clear()
                copas_foram_abridas = False
                primeira_rodada = True
                mensagens_processadas.clear()
                jogadas_na_rodada = 0
                jogador_atual = None

                if ID_JOGADOR == 0:
                    time.sleep(1)
                    distribuir_cartas()
            # reenviar_mensagem(mensagem)  # já está acima

def receber_token_inicial():
    global token_na_mao
    token_na_mao = True

def jogar():
    global token_na_mao, mao, jogador_atual, primeira_rodada, mesa, round_id
    while True:
        if token_na_mao:
            if jogador_atual == ID_JOGADOR and len(mesa) < 4 and mao:
                print(f"\n[Sua vez] Sua mão: {', '.join(mao)}")
                naipe_lider = mesa[0][1][-1] if len(mesa) > 0 else None
                while True:
                    if primeira_rodada and '2♣' in mao and len(mesa) == 0:
                        carta = '2♣'
                        print("Primeira rodada, obrigatório jogar o 2♣.")
                    else:
                        carta = input("Escolha uma carta para jogar: ").strip()
                    if carta not in mao:
                        print("Carta inválida, tente novamente.")
                        continue
                    if not pode_jogar_carta(carta, mao, naipe_lider, primeira_rodada, copas_foram_abridas):
                        print("Jogada não permitida pelas regras, tente outra carta.")
                        continue
                    break
                mao.remove(carta)
                mensagem = f"JOGADA:{ID_JOGADOR}:{round_id}:{carta}"
                enviar_mensagem(mensagem)
                print(f"Você jogou: {carta}")
                token_na_mao = False
            else:
                token_na_mao = False
            enviar_token()
        time.sleep(0.1)

def enviar_token():
    enviar_mensagem("TOKEN")

threading.Thread(target=escutar, daemon=True).start()
threading.Thread(target=jogar, daemon=True).start()

if (ID_JOGADOR == 0):
    time.sleep(1)
    distribuir_cartas()

while True:
    time.sleep(1)

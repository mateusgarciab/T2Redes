import baralho as br
import random

mao_0 = []
mao_1 = []
mao_2 = []
mao_3 = []
verificaJogadores = [True, True, True, True]
verificaJogo = True

while verificaJogo:
    for i in range(4):
        if verificaJogadores[i]:
            print("teste", i)
    verificaJogo = False
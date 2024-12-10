import baralho as br
import random

acao = int(input())
print(acao)

maos = [[], [], [], []]
maos[0].append(1)
maos[0].append(2)
maos[0].append(3)

maos[1].append(1)
maos[1].append(2)

maos[3].append(1)

for i in range(len(maos)):
    for j in range(len(maos[i])):
        print(maos[i][j])
        
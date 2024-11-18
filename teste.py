import baralho as br
import random

baralho = br.criaBaralho()

mao = []
mao.append(br.cartaAleatoria(baralho))
br.imprimeCarta(mao[0])
teste = br.verificaMao(mao)
print(teste)
print(br.valorMao(mao))

mao.append(br.cartaAleatoria(baralho))
br.imprimeCarta(mao[1])
teste = br.verificaMao(mao)
print(teste)
print(br.valorMao(mao))

mao.append(br.cartaAleatoria(baralho))
br.imprimeCarta(mao[2])
teste = br.verificaMao(mao)
print(teste)
print(br.valorMao(mao))

mao.append(br.cartaAleatoria(baralho))
br.imprimeCarta(mao[3])
teste = br.verificaMao(mao)
print(teste)
print(br.valorMao(mao))
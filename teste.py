import baralho as br
import random

baralho = br.criaBaralho()

for i in baralho:
    print(i.simbolo, i.naipe)

cartaEscolhida = br.cartaAleatoria(baralho)

print("você recebeu", cartaEscolhida.simbolo, "de", cartaEscolhida.naipe)

for i in baralho:
    print(i.simbolo, i.naipe)
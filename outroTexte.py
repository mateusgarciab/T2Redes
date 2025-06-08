from baralho import *
from mensagem import *
from jogo import *

msg = Mensagem(5, 1, 15, 50)
jogo = Jogador("eu")
copas_quebradas = False

jogo.mao = criaBaralho()
""" carta = escolheCarta(baralho) """
cartasNaMesa = []
""" cartasNaMesa.append(Carta("copas", 1, 1, 1)) """
jogo.jogadorJoga(cartasNaMesa, 2, copas_quebradas)

print("\nFala ")
imprimeMao(jogo.mao)

""" carta.imprimeCarta() """
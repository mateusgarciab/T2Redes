from baralho import *
from mensagem import *

msg = Mensagem(5, 1, 15, 88)

baralho = criaBaralho()

carta = buscarCartaPorId(int(msg.cartaID), baralho)
carta.imprimeCarta()
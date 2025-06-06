from baralho import *
from mensagem import *

msg = Mensagem(5, 1, 15, 50)

baralho = criaBaralho()
carta = buscarCartaPorId(msg.cartaID, baralho)
print(f"Id {msg.cartaID} {type(msg.cartaID)} {type(carta)}")

carta.imprimeCarta()
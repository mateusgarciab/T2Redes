import baralho as br
import random
import envioRecebido as enre
import pickle

carta = br.Carta("ouros",2)
bloco = enre.Bloco(carta, 0, 1, 0)
mensagem = enre.Mensagem(5, bloco, enre.Bloco(br.Carta("Espada", 15), 1, 2, 3), ((0,0),0,3,0), ((0,0),0,4,0))
br.imprimeCarta(mensagem.bloco1.carta)
comprimido = pickle.dumps(mensagem)
descomprimido = pickle.loads(comprimido)
br.imprimeCarta(descomprimido.bloco1.carta)
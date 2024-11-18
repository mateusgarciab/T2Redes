import random

class Carta:
    def __init__(self, naipe, simbolo):
        self.naipe = naipe
        self.simbolo = simbolo

def criaBaralho():
    baralho = []
    for i in range(10):
        baralho.append(Carta("Espada", i+1))
    baralho.append(Carta("Espada", "Rei"))
    baralho.append(Carta("Espada", "Valete"))
    baralho.append(Carta("Espada", "Dama"))

    for i in range(10):
        baralho.append(Carta("Ouros", i+1))
    baralho.append(Carta("Ouros", "Rei"))
    baralho.append(Carta("Ouros", "Valete"))
    baralho.append(Carta("Ouros", "Dama"))
    
    for i in range(10):
        baralho.append(Carta("Copas", i+1))
    baralho.append(Carta("Copas", "Rei"))
    baralho.append(Carta("Copas", "Valete"))
    baralho.append(Carta("Copas", "Dama"))

    for i in range(10):
        baralho.append(Carta("Paus", i+1))
    baralho.append(Carta("Paus", "Rei"))
    baralho.append(Carta("Paus", "Valete"))
    baralho.append(Carta("Paus", "Dama"))

    return baralho

def cartaAleatoria(baralho):
    random.shuffle(baralho)
    cartaEscolhida = baralho[0]
    baralho.remove(cartaEscolhida)

    return cartaEscolhida

def valorMao(mao):
    valor = 0
    numAs = 0
    numReiDamVal = 0
    for i in range(len(mao)):
        if i.simbolo == "Rei" or i.simbolo == "Valete" or i.simbolo == "Dama":
            numReiDamVal += 1
        elif i.simbolo == 1:
            numAs += 1
        else:
            valor += i.simbolo
        
    if numAs > 0 and numReiDamVal > 0:
        valor += 10*numAs

    return valor
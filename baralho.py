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
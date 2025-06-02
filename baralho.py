import random

class Carta: #revisado
    def __init__(self, naipe, simbolo, valor, identificador):
        self.naipe = naipe
        self.simbolo = simbolo
        self.valor = valor
        self.identificador = identificador

    def imprimeCarta(self): #revisado    
        print(f"{self.simbolo} de {self.naipe} e id {self.identificador}")


def imprimeMao(mao): #revisado
    for i in range(len(mao)):
        mao[i].imprimeCarta()
    print("Valor da mao", valorMao(mao))

def criaBaralho(): #revisado
    baralho = []
    for i in range(9):
        baralho.append(Carta("Espada", i+2, 0, i))
    baralho.append(Carta("Espada", "Rei", 0, 9))
    baralho.append(Carta("Espada", "Valete", 0, 10))
    baralho.append(Carta("Espada", "Dama", 13, 11))
    baralho.append(Carta("Espada", "As", 0, 12))

    for i in range(9):
        baralho.append(Carta("Ouros", i+2, 0, i + 13))
    baralho.append(Carta("Ouros", "Rei", 0, 22))
    baralho.append(Carta("Ouros", "Valete", 0, 23))
    baralho.append(Carta("Ouros", "Dama", 0, 24))
    baralho.append(Carta("Ouros", "As", 0, 25))
    
    for i in range(9):
        baralho.append(Carta("Copas", i+2, 1, i + 26))
    baralho.append(Carta("Copas", "Rei", 1, 35))
    baralho.append(Carta("Copas", "Valete", 1, 36))
    baralho.append(Carta("Copas", "Dama", 1, 37))
    baralho.append(Carta("Copas", "As", 1, 38))

    for i in range(9):
        baralho.append(Carta("Paus", i+2, 0, i + 39))
    baralho.append(Carta("Paus", "Rei", 0, 48))
    baralho.append(Carta("Paus", "Valete", 0, 49))
    baralho.append(Carta("Paus", "Dama", 0, 50))
    baralho.append(Carta("Paus", "As", 0, 51))

    return baralho

""" def cartaAleatoria(baralho): 
    random.shuffle(baralho)
    cartaEscolhida = baralho[0]
    baralho.remove(cartaEscolhida)

    return cartaEscolhida """

def valorMao(mao): #revisado
    valor = 0
    for i in range(len(mao)):
        valor += mao[i].valor

    return valor

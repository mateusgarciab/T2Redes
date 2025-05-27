import random

class Carta: #revisado
    def __init__(self, naipe, simbolo, valor):
        self.naipe = naipe
        self.simbolo = simbolo
        self.valor = valor

    def imprimeCarta(self): #revisado    
        print(f"{self.simbolo} de {self.naipe} com valor {self.valor}")

def imprimeMao(mao): #revisado
    for i in range(len(mao)):
        mao[i].imprimeCarta()
    print("Valor da mao", valorMao(mao))

def criaBaralho(): #revisado
    baralho = []
    for i in range(9):
        baralho.append(Carta("Espada", i+2, 0))
    baralho.append(Carta("Espada", "Rei", 0))
    baralho.append(Carta("Espada", "Valete", 0))
    baralho.append(Carta("Espada", "Dama", 13))
    baralho.append(Carta("Espada", "As", 0))

    for i in range(9):
        baralho.append(Carta("Ouros", i+2, 0))
    baralho.append(Carta("Ouros", "Rei", 0))
    baralho.append(Carta("Ouros", "Valete", 0))
    baralho.append(Carta("Ouros", "Dama", 0))
    baralho.append(Carta("Ouros", "As", 0))
    
    for i in range(9):
        baralho.append(Carta("Copas", i+2, 1))
    baralho.append(Carta("Copas", "Rei", 1))
    baralho.append(Carta("Copas", "Valete", 1))
    baralho.append(Carta("Copas", "Dama", 1))
    baralho.append(Carta("Copas", "As", 1))

    for i in range(9):
        baralho.append(Carta("Paus", i+2, 0))
    baralho.append(Carta("Paus", "Rei", 0))
    baralho.append(Carta("Paus", "Valete", 0))
    baralho.append(Carta("Paus", "Dama", 0))
    baralho.append(Carta("Paus", "As", 0))

    return baralho

def cartaAleatoria(baralho): 
    random.shuffle(baralho)
    cartaEscolhida = baralho[0]
    baralho.remove(cartaEscolhida)

    return cartaEscolhida

def valorMao(mao): #revisado
    valor = 0
    for i in range(len(mao)):
        valor += mao[i].valor

    return valor

def verificaMao(mao):
    if valorMao(mao) > 21:
        return False
    return True

baralho = criaBaralho()
imprimeMao(baralho)
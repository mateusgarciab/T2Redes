class Jogador:
    def __init__(self, numero):
        self.numero = numero
        self.pontos = 0

    def imprimeJog(self):
        self.pontos += 1
        print(f"Tenho número {self.numero} e pontos {self.pontos}")

jog = Jogador(0)
jog.imprimeJog()
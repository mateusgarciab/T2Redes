import random
from baralho import *

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.mao = []
        self.pontosTotais = 0
        self.pontosRodada = 0
    
    def receber_carta(self, carta):
        self.mao.append(carta)
    
    def jogar_carta(self, carta_idx):
        return self.mao.pop(carta_idx)
    
    def ordenar_mao(self):
        self.mao.sort(key=lambda x: x.identificador)
    
    def mostrar_mao(self):
        print(f"\nMão de {self.nome}:")
        """imprimeMao(self.mao)"""

class JogoCopas:
    def __init__(self):
        self.jogadores = []
        self.baralho = criaBaralho()
        self.rodada = 0
        self.cartas_na_mesa = []
        self.jogador_iniciante = 0
        self.copas_quebradas = False
    
    def adicionar_jogador(self, nome):
        if len(self.jogadores) < 4:
            self.jogadores.append(Jogador(nome))
            return True
        return False
    
    
    def distribuir_cartas(self):
        random.shuffle(self.baralho)
        for i in range(len(self.baralho)):
            self.jogadores[i % 4].receber_carta(self.baralho[i])
            """Mandar para o jogador a acrta dele e esperar resposta"""
            """Quem tem o dois de copas"""
            if self.baralho[i].identificador == 26: 
                j = i
        
        for jogador in self.jogadores:
            jogador.ordenar_mao()
        """Retorna o jogador que tem o dois de paus"""
        return j
    
    def iniciar_rodada(self):
        self.rodada += 1
        self.cartas_na_mesa = []
        print(f"\n=== Rodada {self.rodada} ===")

    def iniciaMesa(self):
        self.baralho = criaBaralho()
        self.rodada = 0
        self.cartas_na_mesa = []
        self.jogador_iniciante = 0
        self.copas_quebradas = False
    
    def validar_jogada(self, jogador_idx, carta_idx):
        carta = self.jogadores[jogador_idx].mao[carta_idx]
        
        # Primeira carta da rodada
        if not self.cartas_na_mesa:
            # Na primeira jogada da partida, não pode jogar copas ou dama de espadas
            if self.rodada == 1 and len(self.jogadores[0].mao) == 13:
                if carta.naipe == "Copas" or (carta.naipe == "Espada" and carta.simbolo == "Dama"):
                    return False
            return True
        
        # Verifica se tem cartas do naipe inicial
        naipe_inicial = self.cartas_na_mesa[0].naipe
        tem_naipe = any(c.naipe == naipe_inicial for c in self.jogadores[jogador_idx].mao)
        
        if tem_naipe:
            return carta.naipe == naipe_inicial
        else:
            # Se não tem o naipe, pode jogar qualquer carta
            # Mas não pode iniciar copas até serem "quebradas"
            if not self.copas_quebradas and carta.naipe == "Copas":
                return False
            return True
        
    def simular_escolha(self, jogador):
        # Simula a escolha de carta pelo jogador
        # Isso será substituído pela entrada do jogador
        cartas_validas = []
        for i, carta in enumerate(jogador.mao):
            if self.validar_jogada(self.jogadores.index(jogador), i):
                cartas_validas.append(i)
        
        if not cartas_validas:
            # Se não há jogadas válidas (teoricamente impossível nas regras)
            return 0
        
        return random.choice(cartas_validas)
        
    def jogar_rodada(self):
        self.cartas_na_mesa = []
        self.jogadores_na_rodada = {}  # Novo: mapeia carta -> jogador

        for i in range(4):
            jogador_idx = (self.jogador_iniciante + i) % 4
            jogador = self.jogadores[jogador_idx]

            jogador.mostrar_mao()
            carta_idx = self.simular_escolha(jogador)
            carta_jogada = jogador.jogar_carta(carta_idx)

            self.cartas_na_mesa.append(carta_jogada)
            self.jogadores_na_rodada[carta_jogada] = jogador  # Novo: registra jogador

            print(f"{jogador.nome} jogou: {carta_jogada.simbolo} de {carta_jogada.naipe}")

            if carta_jogada.naipe == "Copas" and not self.copas_quebradas:
                self.copas_quebradas = True
                print("Copas foram quebradas!")

    def determinar_vencedor_rodada(self):
        naipe_inicial = self.cartas_na_mesa[0].naipe
        print("\n---Fim de rodada---")
        """print(naipe_inicial)"""

        cartas_do_naipe = [c for c in self.cartas_na_mesa if c.naipe == naipe_inicial]
        """imprimeMao(cartas_do_naipe)"""

        carta_vencedora = max(cartas_do_naipe, key=lambda x: x.identificador)
        carta_vencedora.imprimeCarta()

        jogador_vencedor = self.jogadores_na_rodada[carta_vencedora]  # Novo: busca direta

        print(f"{jogador_vencedor.nome} venceu a rodada!")

        # Restante do código permanece igual...
        pontos_rodada = sum(1 for c in self.cartas_na_mesa if c.naipe == "Copas")
        dama_espadas = any(c.naipe == "Espada" and c.simbolo == "Dama" for c in self.cartas_na_mesa)

        if dama_espadas:
            pontos_rodada += 13
            print("Dama de Espadas capturada! +13 pontos")

        jogador_vencedor.pontosRodada += pontos_rodada
        self.jogador_iniciante = self.jogadores.index(jogador_vencedor)



    
    def verificaFimMesa(self):
        return all(len(j.mao) == 0 for j in self.jogadores)
    
    def determinarVencedorJogo(self):
        menor_pontuacao = min(j.pontosTotais for j in self.jogadores)
        vencedores = [j for j in self.jogadores if j.pontosTotais == menor_pontuacao]
        
        if len(vencedores) == 1:
            print(f"\n{vencedores[0].nome} venceu o jogo com {vencedores[0].pontosTotais} pontos!")
        else:
            print("\nEmpate entre:")
            for v in vencedores:
                print(f"{v.nome} com {v.pontosTotais} pontos")
        
        return vencedores
    
    def somaPontos(self):
        if any(j.pontosRodada == 26 for j in self.jogadores): # Verificar
            print("\nLua acertada")
            for i in self.jogadores:
                if i.pontosRodada == 26:
                    i.pontosTotais += 0
                else:
                    print(f"Somado 26 em {i.nome}")
                    i.pontosTotais += 26

        else:
            for i in self.jogadores:
                i.pontosTotais += i.pontosRodada
                
        for i in self.jogadores:
            print(f"{i.nome} fez {i.pontosRodada}")
            i.pontosRodada = 0

    def verificaFimJogo(self):
        return any(j.pontosTotais >= 100 for j in self.jogadores)

            

def main():
    jogo = JogoCopas()
    
    # Adiciona jogadores (em rede, seriam os jogadores conectados)
    for i in range(4):
        jogo.adicionar_jogador(f"Jogador {i+1}")
    
    while not jogo.verificaFimJogo():
        jogo.iniciaMesa()
            
        # Distribui cartas
        jogo.distribuir_cartas()
        
        # Jogo principal
        while not jogo.verificaFimMesa():
            jogo.iniciar_rodada()
            jogo.jogar_rodada()
            jogo.determinar_vencedor_rodada()

        """jogo.jogadores[1].pontosRodada = 26"""
        jogo.somaPontos()
        """for i in jogo.jogadores:
            print(i.pontosRodada)"""
        for i in jogo.jogadores:
            print(i.pontosTotais)

    # Resultado final
    jogo.determinarVencedorJogo()


if __name__ == "__main__":
    main()
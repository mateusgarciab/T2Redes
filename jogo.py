import random
from baralho import *
from mensagem import *

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
        imprimeMao(self.mao)

    def jogadorJoga(self, cartas_na_mesa, rodada, copasQuebradas):
        cartasValidas = []
        naipeRodada = 0
        if (not cartas_na_mesa) and (rodada == 1):                          # Você é primeiro da primeira rodada
            cartasValidas.append(buscarCartaPorId(39, self.mao)) # Dois de Paus

        elif rodada == 1:                                                   # Primeira rodada, você não é primeiro
            naipeRodada = cartas_na_mesa[0].naipe
            for i in self.mao:
                if (i.valor == 0) and (naipeRodada == i.naipe):             # Não pode ser de copas nem dama de espada
                    cartasValidas.append(i)

        elif not cartas_na_mesa:                                            # Primeiro da rodada, qualquer rodada
            for i in self.mao:
                if i.naipe ==  "Copas":
                    if copasQuebradas:
                        cartasValidas.append(i)
                else:
                    cartasValidas.append(i)

        else:                                                               # Você não é o primeiro e nem é a primeira rodada
            naipeRodada = cartas_na_mesa[0].naipe
            for i in self.mao:
                if naipeRodada == i.naipe:
                    cartasValidas.append(i)


        if not cartasValidas:                      # Você não tem cartas do naipe da rodada
            for i in self.mao:
                cartasValidas.append(i)

        cartaEscolhida = escolheCarta(cartasValidas)
        # Remove da Mão a carta escolhida
        self.mao = [carta for carta in self.mao if carta.identificador != cartaEscolhida.identificador]
        if cartaEscolhida.naipe == "Copas" and not copasQuebradas:
            copasQuebradas = True
        cartaEscolhida.origem = 1
        cartas_na_mesa.append(cartaEscolhida)
        return cartaEscolhida.identificador
        

class JogoCopas:
    def __init__(self):
        """ self.jogoAtivo = True  """
        self.jogadores = []
        self.baralho = criaBaralho()
        self.rodada = 0
        self.cartas_na_mesa = []
        self.jogador_iniciante = 0
        self.copas_quebradas = False
        """ self.jogadores_na_rodada = {} """
    
    def adicionar_jogador(self, nome):
        if len(self.jogadores) < 4:
            self.jogadores.append(Jogador(nome))
            return True
        return False
    
    
    def distribuir_cartas(self, ipEnvio, portaEnvio, ipChegada, portaChegada):
        random.shuffle(self.baralho)
        mensagem = Mensagem(1, 1, 1, 0)
        for i in range(len(self.baralho)):
            self.jogadores[i % 4].receber_carta(self.baralho[i])
            # Mandar para o jogador a carta dele e esperar resposta
            mensagem.cartaID = self.baralho[i].identificador
            mensagem.destino = (i % 4) + 1
            mensagem.enviaMensagem(ipEnvio, portaEnvio)
            recebeMensagem(ipChegada, portaChegada)
        
        for jogador in self.jogadores:
            jogador.ordenar_mao()

    
    def iniciar_rodada(self, ipEnvio, portaEnvio, ipChegada, portaChegada):
        self.rodada += 1
        self.cartas_na_mesa = []
        """ self.jogadores_na_rodada = {} """
        print(f"\n=== Rodada {self.rodada} ===")

        mensagem = Mensagem(3, 1, 1, self.rodada)
        mensagem.enviaMensagem(ipEnvio, portaEnvio)
        mensagem = recebeMensagem(ipChegada, portaChegada)

    def iniciaMesa(self, ipEnvio, portaEnvio, ipChegada, portaChegada):
        self.baralho = criaBaralho()
        self.rodada = 0
        self.cartas_na_mesa = []
        self.jogador_iniciante = 0
        self.copas_quebradas = False

        mensagem = Mensagem(2, 1, 1, 0)
        mensagem.enviaMensagem(ipEnvio, portaEnvio)
        mensagem = recebeMensagem(ipChegada, portaChegada)
    
    """ def validar_jogada(self, jogador_idx, carta_idx):
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
            return True """
        
    """ def simular_escolha(self, jogador):
        # Simula a escolha de carta pelo jogador
        # Isso será substituído pela entrada do jogador
        cartas_validas = []
        for i, carta in enumerate(jogador.mao):
            if self.validar_jogada(self.jogadores.index(jogador), i):
                cartas_validas.append(i)
        
        if not cartas_validas:
            # Se não há jogadas válidas (teoricamente impossível nas regras)
            return 0
        
        return random.choice(cartas_validas) """
        
    def jogar_rodada(self, jogador, idCarta):
        """ self.cartas_na_mesa = [] """
          # Mapeia carta -> jogador

        jogador = self.jogadores[jogador]

        baralho = criaBaralho()
        carta_jogada = buscarCartaPorId(idCarta, baralho)

        self.cartas_na_mesa.append(carta_jogada)
        """ self.jogadores_na_rodada[carta_jogada] = jogador """ 
        carta_jogada.origem = int(jogador.nome[-1])  # Registra jogador

        print(f" -- {jogador.nome} jogou: {carta_jogada.simbolo} de {carta_jogada.naipe}")
        if carta_jogada.naipe == "Copas" and not self.copas_quebradas:
            self.copas_quebradas = True
            print("Copas foram quebradas!")

    def encontraDoisCopas(self):
        for i in range(len(self.jogadores)):
            for j in self.jogadores[i].mao:
                if j.identificador == 39:
                    return i+1
    

    def determinar_vencedor_rodada(self, ipEnvio, portaEnvio, ipChegada, portaChegada):
        naipe_inicial = self.cartas_na_mesa[0].naipe
        print("\n---Fim de rodada---")
        """print(naipe_inicial)"""

        cartas_do_naipe = [c for c in self.cartas_na_mesa if c.naipe == naipe_inicial]
        """imprimeMao(cartas_do_naipe)"""

        carta_vencedora = max(cartas_do_naipe, key=lambda x: x.identificador)
        carta_vencedora.imprimeCarta()


        jogador_vencedor = self.jogadores[carta_vencedora.origem-1] # -1 por maquinas começarem em 1

        print(f"{jogador_vencedor.nome} venceu a rodada!")

        pontos_rodada = sum(1 for c in self.cartas_na_mesa if c.naipe == "Copas")
        dama_espadas = any(c.naipe == "Espada" and c.simbolo == "Dama" for c in self.cartas_na_mesa)

        if dama_espadas:
            pontos_rodada += 13
            print("Dama de Espadas capturada! +13 pontos")

        jogador_vencedor.pontosRodada += pontos_rodada
        self.jogador_iniciante = self.jogadores.index(jogador_vencedor) + 1 
        
        mensagem = Mensagem(6, 1, 1, int(jogador_vencedor.nome[-1]))
        mensagem.enviaMensagem(ipEnvio, portaEnvio)
        mensagem = recebeMensagem(ipChegada, portaChegada)

        if int(jogador_vencedor.nome[-1]) == 1:
                print("\n++++++++++++ Você ganhou ++++++++++++")
        else:
            print(f"\n++++++++++++ {int(jogador_vencedor.nome[-1])} ganhou ++++++++++++")


    
    def verificaFimMesa(self):
        return all(len(j.mao) == 0 for j in self.jogadores)
    
    def determinarVencedorJogo(self, ipEnvio, portaEnvio):
        menor_pontuacao = min(j.pontosTotais for j in self.jogadores)
        vencedores = [j for j in self.jogadores if j.pontosTotais == menor_pontuacao]
            
        print(f"\n{vencedores[0].nome} venceu o jogo com {vencedores[0].pontosTotais} pontos!")
        mensagem = Mensagem(8, 1, int(vencedores[0].nome[-1]), menor_pontuacao)
        mensagem.enviaMensagem(ipEnvio, portaEnvio)
        
        return vencedores
    
    def somaPontos(self):
        if any(j.pontosRodada == 26 for j in self.jogadores): 
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
        return any(j.pontosTotais >= 30 for j in self.jogadores) # 100 numero de pontos para a cabar o jogo

            

""" def main():
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

        jogo.jogadores[1].pontosRodada = 26
        jogo.somaPontos()
        for i in jogo.jogadores:
            print(i.pontosRodada)
        for i in jogo.jogadores:
            print(i.pontosTotais)

    # Resultado final
    jogo.determinarVencedorJogo()


if __name__ == "__main__":
    main() """
import envioRecebido as enre
import baralho as br
import info
#import copy

ordem = int(input("Digite sua ordem na rodada (1 a 4) "))

valores = info.obter_valores_maquina(ordem - 1)

ipChegada = valores[0]
ipEnvio =  valores[1]
portaRecebe = valores[2]
portaEnvia =   valores[3]


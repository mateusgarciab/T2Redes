def obter_valores_maquina(numero):
    try:
        with open('maquinas.txt', 'r') as arquivo:
            conteudo = arquivo.read()

        maquinas = conteudo.strip().split('\n\n') # Divide em blocos, separados por \n\n
        dados_maquina = maquinas[numero - 1].split('\n') # Seleciona o bloco correspondente a máquina
        
        valores = [linha.split()[1] for linha in dados_maquina[1:]]
        return valores
        
    except FileNotFoundError:
        print("Arquivo 'maquinas.txt' não encontrado.")
        return None

numero_maquina = 2
valores = obter_valores_maquina(numero_maquina)
if valores:
    print(f"Valores da Máquina {numero_maquina}:")
    print(valores)

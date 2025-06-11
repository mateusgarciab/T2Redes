import sys
import os

# Constantes para Hamming(31,26)
N_TOTAL_BITS = 31
K_DATA_BITS = 26
R_PARITY_BITS = N_TOTAL_BITS - K_DATA_BITS # Should be 5

# Gera as posições (1-indexadas) dos bits de paridade e dados
PARITY_POSITIONS_1_INDEXED = []
DATA_POSITIONS_1_INDEXED = []
for i in range(1, N_TOTAL_BITS + 1):
    if (i & (i - 1)) == 0:  # É uma potência de 2
        PARITY_POSITIONS_1_INDEXED.append(i)
    else:
        DATA_POSITIONS_1_INDEXED.append(i)

def hamming_encode_block(data_bits_26_list_int):
    """
    Codifica um bloco de 26 bits de dados para um bloco de 31 bits Hamming.
    data_bits_26_list_int: lista de 26 inteiros (0 ou 1).
    Retorna: string de 31 bits codificados.
    """

    # Verifica se o bloco passado tem realmente 26 bits
    if len(data_bits_26_list_int) != K_DATA_BITS:
        raise ValueError(f"O bloco de dados deve ter {K_DATA_BITS} bits.")

    # Cria um lista com 31 zeros para armazenar o bloco codificado em hamming
    codeword = [0] * N_TOTAL_BITS  # 0-indexado

    # Insere os bits de dados nas posições corretas, ou seja, nas posições diferentes de potências de 2
    data_idx = 0
    for pos_1_indexed in DATA_POSITIONS_1_INDEXED:
        codeword[pos_1_indexed - 1] = data_bits_26_list_int[data_idx]
        data_idx += 1

    # Núcleo da codificação Hamming
    for p_idx in range(R_PARITY_BITS): # Para P1, P2, P4, P8, P16

        # Busca com base no index fornecido pelo for qual a posição real do bit de paridade
        parity_pos_1_indexed = PARITY_POSITIONS_1_INDEXED[p_idx] # 1, 2, 4, 8, 16

        xor_sum = 0

        # Itera sobre todos os bits do codeword para verificar quais são cobertos por este bit de paridade
        for bit_pos_1_indexed in range(1, N_TOTAL_BITS + 1):

            # Não inclua o próprio bit de paridade no cálculo inicial do XOR
            if bit_pos_1_indexed == parity_pos_1_indexed:
                continue
            
            # Se o p_idx-ésimo bit da posição bit_pos_1_indexed for 1, ele é coberto
            if (bit_pos_1_indexed >> p_idx) & 1:
                xor_sum ^= codeword[bit_pos_1_indexed - 1]
        
        codeword[parity_pos_1_indexed - 1] = xor_sum
        
    # Transforma a lista de 31 bits 'codeword' em uma string e retorna
    return "".join(map(str, codeword))

def hamming_decode_block(codeword_31_str):
    """
    Decodifica um bloco Hamming de 31 bits, corrigindo um erro de 1 bit, se houver.
    codeword_31_str: string de 31 bits recebidos.
    Retorna: string de 26 bits de dados corrigidos.
    """
    if len(codeword_31_str) != N_TOTAL_BITS:
        raise ValueError(f"O bloco codificado deve ter {N_TOTAL_BITS} bits.")

    # Transforma a string de 31 bits recebida como parâmetro para uma lista de 31 elementos, podendo cada elemento ser 0 ou 1
    received_codeword_int = [int(b) for b in codeword_31_str]
    
    error_position_1_indexed = 0 # 0 significa nenhum erro detectado

    # Calculo das 5 paridades 
    for p_idx in range(R_PARITY_BITS): # Para P1, P2, P4, P8, P16
        parity_pos_1_indexed = PARITY_POSITIONS_1_INDEXED[p_idx]
        xor_sum = 0

        # Itera sobre todos os bits do codeword que são cobertos por este bit de paridade
        # (incluindo o próprio bit de paridade)
        for bit_pos_1_indexed in range(1, N_TOTAL_BITS + 1):
            # Faz um deslocamento entre 0 e 4 digitos para a direita, dependendo de qual o valor de p_idx atual
            # Depois faz um E (bit a bit) com o valor 1, que resulta em 1 se o bit mais a direita de 'bit_pos_1_indexed' for 1, caso contrario é 0
            # Tudo isso é para fazer a verificação se aquela posição deve ser verificada por aquela paridade
            if (bit_pos_1_indexed >> p_idx) & 1:
                # Faz a verificação da paridade (Se temos numero par de 1's entao o resultado é 0, caso contrario é 1)
                # Retira 1 pois é indexado o começo e 1, e não em 0 como na lista
                xor_sum ^= received_codeword_int[bit_pos_1_indexed - 1]
        
        if xor_sum != 0: # Se a soma XOR é 1, esta paridade falhou
            error_position_1_indexed += parity_pos_1_indexed

    # 2. Corrige o erro, se encontrado
    if error_position_1_indexed > 0 and error_position_1_indexed <= N_TOTAL_BITS:
        # Inverte o bit na posição do erro (0-indexado)
        received_codeword_int[error_position_1_indexed - 1] ^= 1

    # 3. Extrai os bits de dados
    data_bits_extracted = []
    for pos_1_indexed in DATA_POSITIONS_1_INDEXED:
        data_bits_extracted.append(str(received_codeword_int[pos_1_indexed - 1]))
        
    return "".join(data_bits_extracted)

def encode_file(input_filepath, output_filepath):
    """
    Codifica um arquivo de texto usando Hamming(31,26).
    """
    try:
        with open(input_filepath, 'rb') as f_in: # Ler como bytes usando 'rb' = 'read bytes'
            content_bytes = f_in.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo de entrada '{input_filepath}' não encontrado.")
        return

    # Verificação para arquivos vazios
    if not content_bytes:
        with open(output_filepath, 'w') as f_out:
            f_out.write("0\n") # Comprimento original em bits
        print(f"Arquivo de entrada '{input_filepath}' está vazio. Criado '{output_filepath}' vazio.")
        return

    # Transforma cada byte lido é transformado em 8 bits
    bit_string = ""
    for byte_val in content_bytes:
        bit_string += f"{byte_val:08b}" # Converte cada byte para 8 bits

    original_length_in_bits = len(bit_string)

    # Padding com '0's para que o comprimento seja múltiplo de K_DATA_BITS
    # Nesse caso tranforma 'bit_string' em um multiplo de 26 (numero total de posições de dados) 
    num_padding_bits = 0
    if len(bit_string) % K_DATA_BITS != 0:
        # Adiciona quantos 0 são necessarios para ser multiplo de K_DATA_BITS
        # Ex: 26 - (10 % 26) ==> 26 - 16 ==> 10 paddings 
        num_padding_bits = K_DATA_BITS - (len(bit_string) % K_DATA_BITS)
        bit_string += '0' * num_padding_bits

    # Cria os blocos codificados em hamming
    # Transforma os blocos originais de tamanho 26 bits para 31 bits
    encoded_blocks = []
    for i in range(0, len(bit_string), K_DATA_BITS):
        data_block_str = bit_string[i:i+K_DATA_BITS]
        data_block_list_int = [int(b) for b in data_block_str]
        codeword = hamming_encode_block(data_block_list_int)
        encoded_blocks.append(codeword)

    try:
        with open(output_filepath, 'w') as f_out:
            f_out.write(str(original_length_in_bits) + "\n") # Salva o comprimento original
            f_out.write(" ".join(encoded_blocks)) # Salva blocos codificados separados por espaço
        print(f"Arquivo '{input_filepath}' codificado para '{output_filepath}'.")
    except IOError:
        print(f"Erro: Não foi possível escrever no arquivo de saída '{output_filepath}'.")

def decode_file(input_filepath, output_filepath):
    """
    Decodifica um arquivo .hamming para .dec.
    """
    try:
        with open(input_filepath, 'r') as f_in:
            lines = f_in.readlines()
            if not lines:
                print(f"Erro: Arquivo Hamming '{input_filepath}' está vazio ou inválido.")
                open(output_filepath, 'wb').close() # Cria arquivo .dec vazio
                return

            # Salva o valor do tamanho original em bits
            original_length_in_bits_str = lines[0].strip()
            
            # Verifica se é um número / se existe no arquivo
            if not original_length_in_bits_str.isdigit():
                print(f"Erro: Formato inválido em '{input_filepath}'. Comprimento original ausente ou inválido.")
                open(output_filepath, 'wb').close()
                return
            
            original_length_in_bits = int(original_length_in_bits_str)

            if original_length_in_bits == 0:
                 open(output_filepath, 'wb').close() # Cria arquivo .dec vazio
                 print(f"Decodificado para arquivo vazio '{output_filepath}' pois o original era vazio.")
                 return


            # Separa cada bloco de 31 bits como um elemento (string) em uma lista
            codeword_strings = []
            if len(lines) > 1 and lines[1].strip():
                codeword_strings = lines[1].strip().split(' ')
            
            # Filtra strings vazias que podem surgir de múltiplos espaços
            codeword_strings = [cw for cw in codeword_strings if cw]

            if original_length_in_bits > 0 and not codeword_strings:
                 print(f"Aviso: Comprimento original é {original_length_in_bits} mas nenhum bloco codificado foi encontrado em '{input_filepath}'. A saída será vazia/truncada.")
                 # Prosseguir resultará em uma string de bits decodificada vazia/truncada
    
    except FileNotFoundError:
        print(f"Erro: Arquivo Hamming '{input_filepath}' não encontrado.")
        return
    except (IOError, ValueError) as e:
        print(f"Erro ao ler ou processar o arquivo Hamming '{input_filepath}': {e}")
        open(output_filepath, 'wb').close() # Garante que um arquivo .dec seja criado, mesmo que vazio
        return

    # Cria uma string vazia que vai ser a resposta da decodificação
    decoded_bit_stream = ""
    for cw_str in codeword_strings:
        # Verifica se a string que vai decodificada tem 31 bits
        if len(cw_str) != N_TOTAL_BITS:
            if cw_str: # Se não for uma string vazia (já filtrada, mas como segurança)
                print(f"Aviso: Comprimento de bloco codificado inválido encontrado: '{cw_str[:10]}...' (comprimento {len(cw_str)}), esperado {N_TOTAL_BITS}. Ignorando.")
            continue
        try:
            # Chama a função para decodificar a string de 31 bits
            corrected_data_bits_str = hamming_decode_block(cw_str)
            
            # Concatena a string retornada por 'hamming_decode_block' na resposta
            decoded_bit_stream += corrected_data_bits_str
        except ValueError as e:
            print(f"Aviso: Erro ao decodificar bloco '{cw_str[:10]}...': {e}. Ignorando.")


    # Trunca para o comprimento original em bits
    final_bit_stream = decoded_bit_stream[:original_length_in_bits]

    # Converte a string de bits de volta para bytes
    output_bytes = bytearray()
    if final_bit_stream: # Procede apenas se houver bits para converter
        for i in range(0, len(final_bit_stream), 8):
            byte_str = final_bit_stream[i:i+8]
            # Como original_length_in_bits vem de bytes, deve ser múltiplo de 8.
            # Se não for, houve um problema com o valor salvo ou o arquivo está corrompido.
            if len(byte_str) == 8:
                try:
                    output_bytes.append(int(byte_str, 2))
                except ValueError:
                    print(f"Aviso: Segmento de bits inválido '{byte_str}' não pôde ser convertido para byte. Ignorando.")
            # else: # Se o último pedaço não tiver 8 bits, indica um problema com original_length_in_bits
                  # ou com o stream decodificado. Isso não deve acontecer se original_length_in_bits for múltiplo de 8.
                  # print(f"Aviso: Segmento de bits final incompleto '{byte_str}'. Ignorando.")


    try:
        with open(output_filepath, 'wb') as f_out: # Escreve como binário
            f_out.write(output_bytes)
        print(f"Arquivo '{input_filepath}' decodificado para '{output_filepath}'.")
    except IOError:
        print(f"Erro: Não foi possível escrever no arquivo de saída '{output_filepath}'.")


def main():
    if len(sys.argv) < 3:
        print("Uso: python hamming_script.py <encode|decode> <nome_arquivo_original>")
        print("Exemplo (encode): python hamming_script.py encode meu_arquivo.txt")
        print("Exemplo (decode): python hamming_script.py decode meu_arquivo.txt.hamming")
        sys.exit(1)

    operation = sys.argv[1].lower()
    input_filename = sys.argv[2]

    if operation == "encode":
        # nome_original.hamming
        output_filename_hamming = input_filename + ".hamming"
        encode_file(input_filename, output_filename_hamming)
    elif operation == "decode":
        # Espera-se que input_filename seja nome_original.hamming
        # Saída será nome_original.dec
        if not input_filename.endswith(".hamming"):
            print(f"Erro: Para decodificação, o arquivo de entrada ('{input_filename}') deve ter a extensão '.hamming'.")
            sys.exit(1)
        
        base_name_of_hamming = input_filename[:-len(".hamming")] # Remove .hamming
        output_filename_dec = base_name_of_hamming + ".dec"
        decode_file(input_filename, output_filename_dec)
    else:
        print(f"Erro: Operação desconhecida '{operation}'. Use 'encode' ou 'decode'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
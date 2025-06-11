# Jogo de Caça ao Tesouro

Este é um jogo de caça ao tesouro implementado como parte de um trabalho da disciplina de Redes I. O jogo utiliza raw sockets para comunicação entre máquinas e implementa um protocolo personalizado de nível 2.

## Descrição do Jogo

O jogo consiste em um grid 8x8 onde o jogador se move para encontrar tesouros escondidos. Quando um tesouro é encontrado, o servidor envia o arquivo correspondente para o cliente, que o exibe de acordo com seu tipo (texto, imagem ou vídeo).

- O canto inferior esquerdo tem coordenadas (0,0).
- O servidor sorteia 8 posições aleatórias para os tesouros.
- Os tesouros são arquivos de texto (.txt), imagens (.jpg) ou vídeos (.mp4).
- O jogador se move pelo grid usando as teclas W, A, S, D.

## Protocolo de Comunicação

O protocolo implementado é inspirado no Kermit e possui os seguintes campos:

```
| marcador inicio | tamanho | sequencia | tipo | checksum | ... dados ... |
      8 bits         7 bits     5 bits   4 bits  8 bits    0 a 127 bytes
     0111 1110                                   sobre campos
                                                tamanho, seq, tipo e dados
```

### Tipos de Mensagem

- 0: ack
- 1: nack
- 2: ok + ack
- 3: livre
- 4: tamanho
- 5: dados
- 6: texto + ack + nome
- 7: video + ack + nome
- 8: imagem + ack + nome
- 9: fim arquivo
- 10: desloca para direita
- 11: desloca para cima
- 12: desloca para baixo
- 13: desloca para esquerda
- 14: livre
- 15: erro

### Códigos de Erro

- 0: sem permissão de acesso
- 1: espaço insuficiente

## Requisitos

- Linux (testado em 6.8.0-57-generic)
- GCC
- Make
- Permissões de root (para criar e usar raw sockets)
- Duas máquinas conectadas diretamente por cabo de rede

## Instalação e Compilação

1. Clone o repositório ou extraia os arquivos
2. Crie os diretórios necessários:

```bash
make setup
```

3. Compile o código:

```bash
make
```

Isso irá gerar dois executáveis: `treasure_server` e `treasure_client`.

## Preparando o Ambiente

Antes de executar o jogo, você precisa configurar as interfaces virtual Ethernet (veth):

```bash
# Crie as interfaces veth0 e veth1
sudo ip link add veth0 type veth peer name veth1

# Ative as interfaces
sudo ip link set veth0 up
sudo ip link set veth1 up
```

## Preparando os Arquivos de Tesouro

Coloque os arquivos de tesouro no diretório `objetos/`. Os arquivos devem ser nomeados de 1 a 8 com as extensões adequadas:

- Texto: `1.txt`, `2.txt`, etc.
- Imagens: `3.jpg`, `4.jpg`, etc.
- Vídeos: `5.mp4`, `6.mp4`, etc.

## Executando o Jogo

Em uma máquina, execute o servidor:

```bash
sudo ./treasure_server
```

Em outra máquina (ou em outro terminal da mesma máquina para teste), execute o cliente:

```bash
sudo ./treasure_client
```

Alternativamente, você pode usar:

```bash
make run-server
```

e

```bash
make run-client
```

## Como Jogar

No cliente, use os seguintes comandos:

- `W`: Mover para cima
- `S`: Mover para baixo
- `A`: Mover para esquerda
- `D`: Mover para direita
- `Q`: Sair do jogo

Quando o jogador encontra um tesouro, o arquivo é automaticamente exibido.

## Estrutura do Código

- `treasure_protocol.h` e `treasure_protocol.c`: Definições e funções comuns do protocolo
- `treasure_server.c`: Implementação do servidor
- `treasure_client.c`: Implementação do cliente
- `Makefile`: Regras para compilação

## Limitações

- Os nomes dos arquivos podem ter no máximo 63 bytes
- Os arquivos são transferidos em chunks de até 127 bytes
- O jogo usa controle de fluxo por stop-and-wait

## Autores

Implementação de trabalho para a disciplina de Redes I. 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <net/ethernet.h>
#include <netpacket/packet.h>
#include <net/if.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <arpa/inet.h>

#define TAM_PACOTE 1500
#define MARCADOR 0x7E
#define TIPO_DADOS 5

// Função para imprimir um buffer em hexadecimal
void print_buffer(const char* prefix, unsigned char* buffer, int size) {
    printf("%s", prefix);
    for (int i = 0; i < size; i++) {
        printf("%02X ", buffer[i]);
    }
    printf("\n");
}

// Função para calcular o checksum simples
unsigned char calcula_checksum(unsigned char* dados, int tamanho) {
    unsigned short soma = 0;  // Usando unsigned short para evitar overflow
    for (int i = 0; i < tamanho; i++) {
        soma += dados[i];  // Soma os bytes
    }
    return (unsigned char)(soma & 0xFF);  // Retorna apenas o byte menos significativo
}

int main() {
    int sockfd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (sockfd < 0) {
        perror("socket");
        exit(1);
    }

    struct ifreq ifr;
    strncpy(ifr.ifr_name, "veth1", IFNAMSIZ);
    if (ioctl(sockfd, SIOCGIFINDEX, &ifr) == -1) {
        perror("SIOCGIFINDEX");
        exit(1);
    }

    struct sockaddr_ll endereco = {0};
    endereco.sll_family = AF_PACKET;
    endereco.sll_protocol = htons(ETH_P_ALL);
    endereco.sll_ifindex = ifr.ifr_ifindex;

    if (bind(sockfd, (struct sockaddr*)&endereco, sizeof(endereco)) < 0) {
        perror("bind");
        exit(1);
    }

    FILE* out = fopen("recebido.txt", "wb");
    if (!out) {
        perror("Erro ao criar arquivo de saída");
        exit(1);
    }

    printf("Aguardando pacotes...\n");

    unsigned char buffer[TAM_PACOTE];
    while (1) {
        ssize_t n = recvfrom(sockfd, buffer, TAM_PACOTE, 0, NULL, NULL);
        if (n < 0) {
            perror("recvfrom");
            continue;
        }

        if ((size_t)n < sizeof(struct ether_header) + 5) continue;

        struct ether_header *eth = (struct ether_header *)buffer;
        if (ntohs(eth->ether_type) != 0x88B5) continue; // protocolo customizado

        unsigned char *dados = buffer + sizeof(struct ether_header);

        // Verifica se o marcador está presente
        if (dados[0] != MARCADOR) {
            printf("Marcador não encontrado: %02X (esperado: %02X)\n", dados[0], MARCADOR);
            continue;
        }

        // Extrai os dados do pacote
        unsigned char tamanho = dados[1] & 0x7F;  // 7 bits para tamanho
        unsigned char seq     = dados[2] & 0x1F;  // 5 bits para sequência
        unsigned char tipo    = dados[3];         // Tipo do pacote
        unsigned char checksum = dados[4];        // Checksum recebido

        if (tipo != TIPO_DADOS) continue;

        print_buffer("Receptor - Pacote completo: ", dados, 5 + tamanho);
        
        // Cria um buffer temporário para calcular o checksum (excluindo o checksum original)
        unsigned char temp_buffer[TAM_PACOTE];
        memcpy(temp_buffer, dados + 1, 3);            // Copia os 3 bytes de cabeçalho
        memcpy(temp_buffer + 3, dados + 5, tamanho);  // Pula o checksum e copia o restante dos dados
        
        // Imprime dados específicos que entram no cálculo do checksum (exatamente como o emissor)
        printf("Receptor - Dados para checksum (sem o checksum original): ");
        for (int i = 0; i < 3 + tamanho; i++) {
            printf("%02X ", temp_buffer[i]);
        }
        printf("\n");

        // Calcular o checksum exatamente como o emissor
        unsigned char checksum_calculado = calcula_checksum(temp_buffer, 3 + tamanho);

        // Verificar checksum
        printf("Checksum recebido: %02X, Checksum calculado: %02X\n", 
               checksum, checksum_calculado);

        if (checksum != checksum_calculado) {
            fprintf(stderr, "ERRO: Checksum inválido no frame seq %d\n", seq);
            
            // Análise de debug para entender por que houve divergência
            printf("   Tamanho do pacote: %d bytes\n", tamanho);
            printf("   Sequência: %d\n", seq);
            printf("   Tipo: %d\n", tipo);
            continue;
        }

        // Se checksum estiver correto, salva os dados
        fwrite(dados + 5, 1, tamanho, out);
        fflush(out);

        printf("Frame seq %d recebido com sucesso (%d bytes).\n", seq, tamanho);
    }

    fclose(out);
    close(sockfd);
    return 0;
}

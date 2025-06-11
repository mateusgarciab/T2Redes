#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/ether.h>
#include <netpacket/packet.h>
#include <net/if.h>
#include <sys/socket.h>
#include <sys/ioctl.h>

#define MARCADOR 0x7E
#define TAM_DADOS 127
#define TIPO_DADOS 5
#define TAM_PACOTE 1500

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
    // Cria o socket raw
    int sockfd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (sockfd < 0) {
        perror("socket");
        exit(1);
    }

    // Obter índice da interface veth0
    struct ifreq ifr;
    memset(&ifr, 0, sizeof(ifr));
    strncpy(ifr.ifr_name, "veth0", IFNAMSIZ);
    if (ioctl(sockfd, SIOCGIFINDEX, &ifr) == -1) {
        perror("SIOCGIFINDEX");
        exit(1);
    }

    int ifindex = ifr.ifr_ifindex;

    // Endereço do socket (interface de rede veth0)
    struct sockaddr_ll endereco = {0};
    endereco.sll_family = AF_PACKET;
    endereco.sll_ifindex = ifindex;
    endereco.sll_halen = ETH_ALEN;

    // Endereços MAC (destino e origem)
    unsigned char dest_mac[6] = {0xaa, 0xef, 0x89, 0x44, 0x14, 0xd2};  // Exemplo
    unsigned char src_mac[6]  = {0x62, 0x42, 0x03, 0x53, 0xa4, 0x24};  // Exemplo

    memcpy(endereco.sll_addr, dest_mac, 6);  // Define o destino do pacote

    // Abre o arquivo para enviar
    FILE* f = fopen("mensagem.txt", "rb");
    if (!f) {
        perror("Erro ao abrir arquivo");
        exit(1);
    }

    unsigned char buffer[TAM_DADOS];
    unsigned char pacote[1514]; // Tamanho máximo Ethernet
    struct ether_header *eth = (struct ether_header *)pacote;

    memcpy(eth->ether_dhost, dest_mac, 6);  // Endereço MAC de destino
    memcpy(eth->ether_shost, src_mac, 6);   // Endereço MAC de origem
    eth->ether_type = htons(0x88B5);        // Tipo Ethernet personalizado

    int seq = 0;
    size_t lidos;

    // Envia o arquivo em pacotes
    while ((lidos = fread(buffer, 1, TAM_DADOS, f)) > 0) {
        unsigned char *dados = pacote + sizeof(struct ether_header);

        // Prepara o pacote
        dados[0] = MARCADOR;                  // Marcador de início
        dados[1] = lidos & 0x7F;              // Tamanho (7 bits)
        dados[2] = seq & 0x1F;                // Sequência (5 bits)
        dados[3] = TIPO_DADOS;                // Tipo (5 para dados)
        
        // Cria um buffer temporário para calcular o checksum
        unsigned char temp_buffer[TAM_PACOTE];
        memcpy(temp_buffer, dados + 1, 3);           // Copia tamanho, seq e tipo
        memcpy(temp_buffer + 3, buffer, lidos);      // Copia dados do arquivo
        
        // Imprime dados que entram no cálculo do checksum (para debug)
        printf("Emissor - Dados para checksum (sem o checksum): ");
        for (int i = 0; i < 3 + lidos; i++) {
            printf("%02X ", temp_buffer[i]);
        }
        printf("\n");
        
        // Calcula e armazena o checksum
        unsigned char checksum = calcula_checksum(temp_buffer, 3 + lidos);
        dados[4] = checksum;  // Armazena o checksum no pacote
        
        // Copia os dados do arquivo para o pacote (após o cabeçalho)
        memcpy(dados + 5, buffer, lidos);
        
        // Imprime o pacote completo para debug
        print_buffer("Emissor - Pacote completo: ", dados, 5 + lidos);
        
        // Debug: Imprime o checksum calculado
        printf("Pacote seq %d com checksum: %02X\n", seq, checksum);

        // Envia o pacote
        size_t tam_total = sizeof(struct ether_header) + 5 + lidos;
        ssize_t enviados = sendto(sockfd, pacote, tam_total, 0, 
                                (struct sockaddr*)&endereco, sizeof(endereco));
        
        if (enviados < 0) {
            perror("sendto");
            break;
        }

        printf("Enviado frame seq %d (%ld bytes no total, %ld bytes de dados)\n", 
               seq, tam_total, lidos);
               
        // Atualiza sequência e aguarda
        seq = (seq + 1) % 32; // Atualiza o número de sequência de 5 bits
        usleep(200000);       // Delay para simular espera por ACK
    }

    fclose(f);
    close(sockfd);
    printf("Envio completo.\n");

    return 0;
}

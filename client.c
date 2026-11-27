#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib") 

#define PORT 4300
#define BUFFER_SIZE 4096

int main(int argc, char *argv[]) {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];
    char query[256];
    int bytes_received;

  
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("WSAStartup failed.\n");
        return 1;
    }

   
    if (argc != 3) {
        printf("Usage: %s <WSL_IP_ADDRESS> <domain_to_query>\n", argv[0]);
        printf("Example: %s 172.24.144.5 example.com\n", argv[0]);
        WSACleanup();
        return 1;
    }

    const char *wsl_ip = argv[1];
    const char *domain = argv[2];


    sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        printf("Could not create socket: %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }

    
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT); // Convert port to network byte order
    server_addr.sin_addr.s_addr = inet_addr(wsl_ip);

  
    printf("[C Client] Connecting to %s:%d...\n", wsl_ip, PORT);
    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        printf("Connection failed. Is the WSL server running?\n");
        closesocket(sock);
        WSACleanup();
        return 1;
    }

     snprintf(query, sizeof(query), "%s\r\n", domain);
    send(sock, query, strlen(query), 0);
    printf("[C Client] Sent query: %s", query);

   
    printf("\n--- WHOIS Response ---\n");
    memset(buffer, 0, BUFFER_SIZE);
    while ((bytes_received = recv(sock, buffer, BUFFER_SIZE - 1, 0)) > 0) {
        buffer[bytes_received] = '\0'; // Null-terminate
        printf("%s", buffer);
    }

    if (bytes_received == 0) {
        
        printf("\n----------------------\n");
    } else {
        printf("\nrecv failed: %d\n", WSAGetLastError());
    }

    closesocket(sock);
    WSACleanup();
    return 0;
}
WHOIS Protocol Implementation (ITT440 Network Programming)

- Student Name: Amir Hamzah Bin Mohd Hadzir
- Student ID: 2025919913
- Protocol: WHOIS (RFC 3912)
- Port: 43 (Standard) / 4300 (Development)



Project Overview

This project is a custom implementation of the WHOIS protocol (RFC 3912) using raw TCP sockets. It features a Python-based multi-threaded server running on WSL Ubuntu, and a C-based client running on Windows, demonstrating cross-platform network communication. 

Features Implemented
- TCP connection handling on port 4300.
- Proper parsing of CRLF (`\r\n`) terminated query strings.
- JSON-backed simulated WHOIS database.
- Standard text-based response formatting (terminated by a blank line).
- Graceful handling of non-existent domains and empty queries.
- Cross-Platform C Client: The client is written in C using Winsock2, demonstrating raw byte-order conversion (`htons`) and socket handling across different OS environments.

 How to Run

 1. Start the Server (WSL Ubuntu)
Open a terminal in WSL and navigate to the project folder:
```bash
python3 server.py
```
2. Find WSL IP Address
Open Windows PowerShell and run:
```bash
wsl hostname -I
```
3. Run the C Client (Windows)
Compile the C code using GCC (MinGW) in Windows PowerShell:
```bash
gcc client.c -o client.exe -lws2_32 -D_WIN32_WINNT=0x0601
```
4. Run a query (replace the IP with your WSL IP):
```bash
.\client.exe <YOUR_WSL_IP> example.com
```

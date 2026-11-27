#!/usr/bin/env python3
"""
WHOIS Client (RFC 3912)
Sends a query string terminated by CRLF, reads until server closes.
"""

import socket
import sys

HOST = "127.0.0.1"
PORT = 4300

def whois_query(query):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # RFC 3912: query must end with CRLF
        s.sendall((query + "\r\n").encode("utf-8"))

        chunks = []
        while True:
            data = s.recv(4096)
            if not data:
                break
            chunks.append(data)
        return b"".join(chunks).decode("utf-8", errors="replace")

def main():
    if len(sys.argv) > 1:
        query = sys.argv[1]
        print(whois_query(query), end="")
        return

    print(f"WHOIS client -> {HOST}:{PORT} (type 'quit' to exit)")
    while True:
        try:
            q = input("query> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if q.lower() in ("quit", "exit"):
            break
        if not q:
            continue
        print(whois_query(q), end="")

if __name__ == "__main__":
    main()


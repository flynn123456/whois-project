#!/usr/bin/env python3
"""
WHOIS Server Implementation (RFC 3912)
Course: ITT440 Network Programming
Port: 43 standard (using 4300 for testing)
"""

import socket
import json
import logging
from datetime import datetime

HOST = "0.0.0.0"
PORT = 4300          # change to 43 when running with sudo
DB_FILE = "whois_db.json"
LOG_FILE = "whois_queries.log"

# ---------- Logging setup ----------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ---------- Load database ----------
def load_db(path):
    with open(path, "r") as f:
        return json.load(f)

# ---------- Build a WHOIS-style response ----------
def build_response(query, db):
    """
    Returns the text response for a query.
    RFC 3912: response is free-form text, terminated by connection close.
    """
    key = query.strip().lower()
    if not key:
        return "ERROR: Empty query.\r\n"

    record = db.get(key)
    if record is None:
        return f'No match for "{query}".\r\n'

    lines = []
    for field, value in record.items():
        lines.append(f"{field}: {value}")
    # WHOIS responses end with a blank line
    lines.append("")
    return "\r\n".join(lines) + "\r\n"

# ---------- Handle one client ----------
def handle_client(conn, addr, db):
    logging.info(f"Connection from {addr[0]}:{addr[1]}")
    conn.settimeout(10)
    try:
        data = conn.recv(1024)
        if not data:
            return
        # WHOIS query is terminated by CRLF
        query = data.decode("utf-8", errors="replace").split("\r\n")[0]
        logging.info(f"Query: {query!r}")

        response = build_response(query, db)
        conn.sendall(response.encode("utf-8"))
    except socket.timeout:
        logging.info("Client timed out.")
    except Exception as e:
        logging.info(f"Error handling client: {e}")
    finally:
        conn.close()

# ---------- Main loop ----------
def main():
    db = load_db(DB_FILE)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[WHOIS] Server listening on {HOST}:{PORT}")
    print(f"[WHOIS] Loaded {len(db)} records from {DB_FILE}")
    try:
        while True:
            conn, addr = server.accept()
            handle_client(conn, addr, db)
    except KeyboardInterrupt:
        print("\n[WHOIS] Shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    main()

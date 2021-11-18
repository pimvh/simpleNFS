#!/usr/bin/env python3

from clients.tcp_client import EchoTCPClient

def main():
    try:
        EchoTCPClient("127.0.0.1", 8888, 'Hello World!')
    except KeyboardInterrupt:
        print('shutting down!')

if __name__ == "__main__":
    main()
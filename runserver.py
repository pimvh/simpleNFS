#!/usr/bin/env python3
from servers.tcp_server import EchoTCPServer
def main():
    try:
        s = EchoTCPServer("127.0.0.1", 8888)
        s.run()
    except KeyboardInterrupt:
        print('shutting down!')

if __name__ == "__main__":
    main()
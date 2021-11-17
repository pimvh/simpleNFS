#!/usr/bin/env python3
from tcp_echo.tcp_server import EchoTCPSocket
def main():
    try:
        s = EchoTCPSocket("127.0.0.1", 8888)
        s.run()
    except KeyboardInterrupt:
        print('shutting down!')

if __name__ == "__main__":
    main()
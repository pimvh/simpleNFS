#!/usr/bin/env python3
import asyncio

from tcp_echo.tcp_client import tcp_echo_client

def main():
    try:
        asyncio.run(tcp_echo_client("127.0.0.1", 8888, 'Hello World!'))
    except KeyboardInterrupt:
        print('shutting down!')

if __name__ == "__main__":
    main()
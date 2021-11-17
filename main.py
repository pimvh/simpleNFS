#!/usr/bin/env python3
import asyncio

from tcp_echo.tcp_server import simpleserver

def main():
    try:
        asyncio.run(simpleserver('127.0.0.1', '8888'))
    except KeyboardInterrupt:
        print('shutting down!')

if __name__ == "__main__":
    main()
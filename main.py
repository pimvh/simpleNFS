#!/usr/bin/env python3

import asyncio

from .TCP_echo import server

def main():
    asyncio.run(server('127.0.0.1', '8888'))

if __name__ == "__main__":
    main()
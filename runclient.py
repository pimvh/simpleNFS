#!/usr/bin/env python3

import argparse

from clients.tcp_client import EchoTCPClient
from clients.tcp_dgram_client import DatagramTCPClient

def main():

    parser = argparse.ArgumentParser(description='run a client server.')
    parser.add_argument('type', choices=['echo', 'datagram'],
                        help="type of client to run")

    args = parser.parse_args()

    client = {
        'echo'      : EchoTCPClient,
        'datagram'  : DatagramTCPClient,
    }

    try:
        c = client.get(args.type)("145.100.104.42", 8888)
        c.send_and_receive('Hello World!')
    except KeyboardInterrupt:
        print('shutting down!')
        c.close()

if __name__ == "__main__":
    main()
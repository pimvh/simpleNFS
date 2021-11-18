#!/usr/bin/env python3
import argparse
from servers.tcp_dgram_server import DatagramTCPServer
from servers.tcp_server import EchoTCPServer

def main():
    parser = argparse.ArgumentParser(description='run a client server.')
    parser.add_argument('type', choices=['echo', 'datagram'],
                        help="type of server to run")

    args = parser.parse_args()

    server = {
        'echo'      : EchoTCPServer,
        'datagram'  : DatagramTCPServer,
    }

    try:
        s = server.get(args.type)("145.100.104.42", 8888)
        s.run()
    except KeyboardInterrupt:
        print('shutting down!')

if __name__ == "__main__":
    main()
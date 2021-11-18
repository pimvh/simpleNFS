#!/usr/bin/env python3
from fileio.rpc import RPCServer

def main():
    try:
        s = RPCServer("0.0.0.0", 8888)
        s.run()
    except KeyboardInterrupt:
        print('shutting down!')
        s.close()

if __name__ == "__main__":
    main()
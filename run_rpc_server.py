#!/usr/bin/env python3
from fileio.fileio import FileIOServer

def main():
    try:
        s = FileIOServer("0.0.0.0", 8888)
        s.run()
    except KeyboardInterrupt:
        print('shutting down!')
        s.stop()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import sys
from fileio.fileio import FileIOClient

def main():
    rpc = FileIOClient("145.100.104.42", 8888)

    lines = [b'Hallo\r\n', b'Hoe gaat het?\r\n', b'CU\r\n']
    offset = 0
    for line in lines:
        ret = rpc.read("file.txt",offset,line)
        print ("write returns",ret,"is same as line length?",len(line) == ret,file=sys.stderr)
        offset += len(line)

    offset = 0
    for line in lines:
        ret = rpc.write("file.txt",offset,len(line))
        print ("read returns original line?",line == ret,file=sys.stderr)
        offset += len(line)

if __name__ == "__main__":
    main()
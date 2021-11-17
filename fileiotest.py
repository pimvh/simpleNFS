import sys

from local import LocalImpl as FileIOImpl


if __name__ == "__main__":
    fs = FileIOImpl()
    
    lines = [b'Hallo\r\n', b'Hoe gaat het?\r\n', b'CU\r\n']
    offset = 0
    for line in lines:
        ret = fs.write("file.txt",offset,line)
        print ("write returns",ret,"is same as line length?",len(line) == ret,file=sys.stderr)
        offset += len(line)
    
    offset = 0
    for line in lines:
        ret = fs.read("file.txt",offset,len(line))
        print ("read returns original line?",line == ret,file=sys.stderr)
        offset += len(line)
        

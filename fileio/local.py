import os 
from pathlib import Path

class LocalImpl:
    def __init__(self) -> None:
        pass
    
    def read(self, filename : str, offset : int, length : int, **kwargs):
        """ Read data from a file.
        @param filename The file to read from.
        @param offset   The offset to start reading from.
        @param length   The number of bytes to read.
        @return The data read or '' in case of error.
        """

        # if not isinstance(filename, str) or not isinstance(offset, int) or not isinstance(length, int):

        #     filename = str(filename)
        #     offset = int(offset)
        #     length = int(length)
        #     # raise TypeError('Please supply all parameter types correctly')

        if not os.path.isfile(filename):
            return bytes('')

        with open(filename, 'rb') as f:
            if not f.seekable():
                return bytes('')

            f.seek(offset)
            return f.read(length)

        
    def write(self, filename : str, offset : int, block : bytes, **kwargs):
        """ Write data to a file.
        @param filename The file to write to.
        @param offset   The offset to write at.
        @param block    The block of data to write.
        @return The number of bytes written or -1 in case of error.
        """

        # if not isinstance(filename, str) or not isinstance(offset, int) or not isinstance(block, bytearray):
        #     raise TypeError('Please supply all parameter types correctly')

        if not os.path.isfile(filename):
            Path(filename).touch()

        # + mode creates file if it does not exist
        with open(filename, 'r+b') as f:

            if not f.writable():
                return -1

            f.seek(offset)
            f.write(block)

            return len(block)

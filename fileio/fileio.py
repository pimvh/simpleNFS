import json

from fileio.rpc import RPCClient, RPCServer
from fileio.local import LocalImpl

class FileIOClient():
    def __init__(self, 
                 remoteip : str, 
                 remoteport: int) -> None:
        self.rpc = RPCClient(remoteip, remoteport)

    def read(self, filename : str, offset : int, length : bytes) -> str:
        """ Read data from a file.
        @param filename The file to read from.
        @param offset   The offset to start reading from.
        @param length   The number of bytes to read.
        @return The data read or '' in case of error.
        """

        if not isinstance(filename, str) or not isinstance(offset, int) or not isinstance(length, bytes):
            raise TypeError('Please supply all parameter types correctly')

        return self.rpc.read(filename=filename, offset=offset, length=str(length))
       
        
    def write(self, filename : str, offset : int, block : bytes):
        """ Write data to a file.
        @param filename The file to write to.
        @param offset   The offset to write at.
        @param block    The block of data to write.
        @return The number of bytes written or -1 in case of error.
        """

        if not isinstance(filename, str) or not isinstance(offset, int) or not isinstance(block, bytes):
            raise TypeError('Please supply all parameter types correctly')

        return self.rpc.write(filename=filename, offset=offset, block=str(block))


class FileIOServer(LocalImpl):
    def __init__(self, ip : str, port : int) -> None:
        super().__init__()
        self.rpc = RPCServer(ip, port)

    def run(self):
        """ start the server """
        self.rpc.run()

    def stop(self):
        """ stop the server """
        self.rpc.stop()
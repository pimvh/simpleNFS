#
# Helper class send blocks of data unmodified over a TCP connection.
# This is needed because a TCP connection is defined as delivering a stream
# of bytes. This means that if you send 1024 bytes, it may be received as
# 2x 512 bytes at the receiver, or vice versa. Standard procedure is to prefix
# the data with a 4 byte length field in network byte-order.
#
# Usage:
#
#    sock = socket.connect(x) 
#    dc = DatagramConnection(sock)
#    hisdata = dc.recv()
#    dc.send(mydata)
#    dc.close()
#
import struct

class DatagramConnection:
    def __init__(self,sock):
        self.sock = sock
        self.buffer = b''
        
    def send(self,dgram):
        dgramlenbin=struct.pack("!I",len(dgram))
        msg = dgramlenbin+bytearray(dgram,"utf-8")
        self.sock.send(msg)
   
    def recv(self):
        dgramlenbin = self._recvn(4)
        if len(dgramlenbin) == 0:
            return ''
        (dgramlen,) = struct.unpack("!I",dgramlenbin)
        return self._recvn(dgramlen)

    def close(self):
        self.sock.close()

    def _recvn(self,n):
        while len(self.buffer) < n:
            data = self.sock.recv(1024)
            if len(data) == 0:
                return ''
            self.buffer = self.buffer + data
            
        data = self.buffer[:n]
        self.buffer = self.buffer[n:]
        return data

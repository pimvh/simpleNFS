import socket 
import struct

from typing import Callable

from clients.tcp_client import EchoTCPClient

class DatagramTCPClient(EchoTCPClient):
    """ implements a datagram TCP Socket """
    def __init__(self, ip: str, port: int, message : str, process_func : Callable = None) -> None:
        super().__init__(ip, port, message)
        self.buffer = b''
        self.process_func = process_func

        
    def send(self, dgram):
        """ send a number of bytes """
        if not self.sock:
            raise ValueError('No Active Connection!')

        dgramlenbin= struct.pack("!I", len(dgram))
        msg = dgramlenbin + dgram
        self.sock.send(msg)

   
    def recv(self):
        """ receive a number of bytes """
        
        if not self.sock:
            raise ValueError('No Active Connection!')

        dgramlenbin = self._recvn(4)
        
        if not len(dgramlenbin):
            return ''
        
        (dgramlen,) = struct.unpack("!I", dgramlenbin)
        
        return self._recvn(dgramlen)


    def _recvn(self, n):
        """ receive the nth fragment """ 

        while len(self.buffer) < n:
            data = self.sock.recv(1024)
            if not len(data):
                return ''
            self.buffer = self.buffer + data
            
        data = self.buffer[:n]
        self.buffer = self.buffer[n:]

        return data
        
   
    def run(self):
        """ start the Datagram Socket """
        print(f'connecting to {self.ip} port {self.port}')
        self.sock = socket.create_connection((self.ip, self.port))

        # try:
        print(f"sending message: {self.message}")
        self.send(self.message)

        amount_received = 0
        amount_expected = len(self.message)
        
        while amount_received < amount_expected:

            data = self.recv()
            amount_received += len(data)

            print(f'data received {data}')

        if self.process_func:
            self.process_func(data)

        # except Exception as e:
        #     print('handling error!')
        #     print(e)
        # finally:
        #     self.close()
     
    def close(self):
        """ close the connection properly """
        self.sock.close()

            
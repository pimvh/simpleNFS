import struct
from typing import Callable

from .tcp_server import EchoTCPServer 

class DatagramTCPServer(EchoTCPServer):
    """ implements a datagram TCP Socket """
    def __init__(self, ip: str, port: int, process_func : Callable = None) -> None:
        super().__init__(ip, port)
        self.buffer = b''
        self.process_func = process_func
        
    def send(self, dgram):
        """ send a number of bytes """
        if not self.connection:
            raise ValueError('No Active Connection!')

        dgramlenbin = struct.pack("!I", len(dgram))
        msg = dgramlenbin + bytearray(dgram, "utf-8")

        print('sending message...')
        self.connection.send(msg)
        self.connection.close()

   
    def recv(self):
        """ receive a number of bytes """
        
        if not self.connection:
            raise ValueError('No Active Connection!')

        dgramlenbin = self._recvn(4)
        
        if not len(dgramlenbin):
            return ''
        
        (dgramlen,) = struct.unpack("!I", dgramlenbin)
        
        return self._recvn(dgramlen)


    def _recvn(self, n):
        """ receive the nth fragment """ 

        while len(self.buffer) < n:
            data = self.connection.recv(1024)
            if not len(data):
                return ''
            self.buffer = self.buffer + data
            
        data = self.buffer[:n]
        self.buffer = self.buffer[n:]

        return data

    
    def run(self):
        """ start the Datagram Socket """
        print(f'starting up on {self.ip} port {self.port}')
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)

        self.connection = None

        while True: 
            print('accepting connection....')
            self.connection, client_address = self.sock.accept()

            try:
                print(f'incoming connection from {client_address}...')

                data = self.recv()
                print(f'received {data}')
                
                # call the process function
                if self.process_func:
                    self.process_func(data)

            except Exception as e:
                print(e)
                self.close()
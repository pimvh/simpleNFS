import socket 
import struct

from typing import Callable

from clients.tcp_client import EchoTCPClient

class DatagramTCPClient(EchoTCPClient):
    """ implements a datagram TCP Socket """
    def __init__(self, ip: str, port: int) -> None:
        super().__init__(ip, port)
        self.buffer = b''

        
    def send(self, dgram):
        """ send a number of bytes """
        if not self.sock:
            raise ValueError('No Active Connection!')

        dgramlenbin= struct.pack("!I", len(dgram))
        msg = dgramlenbin + bytearray(dgram,"utf-8")
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
        
   
    def send_and_receive(self, message : str):
        """ start the Datagram Socket """
        print(f'connecting to {self.ip} port {self.port}')
        self.sock = socket.create_connection((self.ip, self.port))

        # try:
        print(f"sending message: {message}")
        self.send(message)

        amount_received = 0
        amount_expected = len(message)

        data = ''
        
        while amount_received < amount_expected:

            data += str(self.recv())
            print('here?')
            amount_received += len(data)

            print(f'data received {data}')

        return data

        # except Exception as e:
        #     print('handling error!')
        #     print(e)
        # finally:
        #     self.close()
     
    def close(self):
        """ close the connection properly """
        self.sock.close()

            
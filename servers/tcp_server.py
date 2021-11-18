
"""
    taken from https://pymotw.com/2/socket/tcp.html#echo-server
    made class based, and reorganized code for clarity
"""

import socket

class EchoTCPServer():
    """ class that implements a simple Echo TCP socket """
    def __init__(self, ip : str, port : int) -> None:
        """ initialize the echo TCP socket 
            @param ip adress to run on 
            @param port to run on 
        """
        self.sock : socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.ip = ip 
        self.port = port 
        self.connection = None

    def send(self, data):
        """ send data over the socket """
        if not self.connection:
            raise ValueError('No Active Connection')
        
        self.connection.send(data)

    def recv(self, bytes=16):
        """ receive data from the socket """
        return self.connection.recv(bytes)
    
    def run(self):
        """ start the simple Socket """
        print(f'starting up on {self.ip} port {self.port}')
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)

        self.connection = None

        while True: 
            print('accepting connection....')
            self.connection, client_address = self.sock.accept()

            try:
                print(f'incoming connection from {client_address}...')
                # Receive the data in small chunks and retransmit it

                while True:
                    data = self.recv(16)
                    print(f'received {data}')
                    
                    if data:
                        self.send(data)
                    else:
                        print('no more data.')
                        break
            except Exception as e:
                print(e)
                self.close()
        
    def close(self):
        """ close the connection properly """
        self.connection.close()

"""
    taken from https://pymotw.com/2/socket/tcp.html#echo-server
    made class based, and reorganized code for clarity
"""

import socket

class EchoTCPClient(): 
    """ class that implements a simple Echo TCP socket Client """
    def __init__(self, ip : str, port : int) -> None:
        """ initialize the echo TCP socket 
            @param ip adress to run on 
            @param port to run on 
        """
        self.sock : socket.socket = None

        self.ip = ip 
        self.port = port 


    def send(self, data):
        """ send data over the socket """
        if not self.sock:
            raise ValueError('No Active Connection')
        
        self.sock.send(data)


    def recv(self, bytes=16):
        """ receive data from the socket """
        return self.sock.recv(bytes)
    

    def send_and_receive(self, message):
        """ start the simple Socket """
        print(f'connecting to {self.ip} port {self.port}')
        self.sock = socket.create_connection((self.ip, self.port))

        try:

            message = message.encode()

            print(f"sending message: {message}")
            self.sock.sendall(message)

            amount_received = 0
            amount_expected = len(message)
            
            while amount_received < amount_expected:
                data = self.recv()
                amount_received += len(data)
                print(f"received: {data}")

        except Exception as e:
            print(e)
        finally:
            self.close()
 

    def close(self):
        """ close the connection properly """
        self.sock.close()
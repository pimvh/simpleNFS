import json
import uuid

from clients.tcp_dgram_client import DatagramTCPClient

from fileio.local import LocalImpl
from servers.tcp_dgram_server import DatagramTCPServer


class RPCBase:
    def __init__(self) -> None:

        default_keys = {'type', 'id', 'filename', 'offset'}

        self.required_keys = {
            'read'  : default_keys & {'length'},
            'write' : default_keys & {'block'},
        }


    @staticmethod
    def _encode(data : dict) -> hex:
        """ dump the dict as a json """

        if 'block' in data:
            data['block'] = data['block'].hex()
            print(data['block'])
        
        if 'data' in data:
            data['data'] = data['data'].hex()
            print(data['data'])

        return json.dumps(data)


    @staticmethod
    def _decode(data : bytes) -> dict:
        """ parse the dict from the json """
        
        data = json.loads(data)
        
        if 'block' in data:
            data['block'] = bytes.fromhex(data['block'])
            assert isinstance(data['block'], bytes)

        if 'data' in data:
            data['data'] = bytes.fromhex(data['data'])
            assert isinstance(data['data'], bytes)
        

        return data

class RPCClient(RPCBase):
    """ implementation of an RPC client, depends on
        the RPC base 
    """
    def __init__(self, ip, port) -> None:
        """ @params ip to run on 
            @params port to run on
        """
        super().__init__()
        self.socket : DatagramTCPClient = DatagramTCPClient(ip, port)
    

    def _send_call(self, call) -> dict:
        """ send a RPC over the network,
            returns an answer to that call """

        data = self.socket.send_and_receive(call)
        return self._decode(data)

    def read(self, **kwargs):
        """ send data to the socket, and decode the reply
            @param dict with the necessary write params
        """

        id = str(uuid.uuid4())

        reply = self._send_call(self._encode(dict(type='read',
                                                  id=id,
                                                  **kwargs)))

        if not reply.get('id') == id:
            raise ValueError('Received reply with other UUID!')

        return reply.get('data', '')


    def write(self, **kwargs):
        """ send data to the socket, and decode the reply
            @param dict with the necessary write params
        """

        id = str(uuid.uuid4())

        reply = self._send_call(self._encode(dict(type='write',
                                                  id=id,
                                                  **kwargs)))

        if not reply.get('id') == id:
            raise ValueError('Received reply with other UUID!')

        return reply.get('written', '')


class RPCServer(RPCBase, LocalImpl):
    """ implementation of an RPC server, depends on the local implementation 
        and the RPC base 
    """
    def __init__(self, ip, port) -> None:
        """ @params ip to run on 
            @params port to run on
        """
        super().__init__()

        self.socket = DatagramTCPServer(ip, port, self.make_reply)

        self.implemented_calls = {
            'read'  : self.handle_read,
            'write' : self.handle_write,
        }


    def run(self) -> None:
        """ start the underlying socket """
        self.socket.run()

    def stop(self) -> None:
        """ stop the underlying socket """
        self.socket.close()


    def make_reply(self, data) -> None:
        """ figure out what to reply based on incoming TCP data 
            @param the incoming call 
        """

        made_call = self._decode(data)

        if not 'type' in made_call:
            return ''

        type_of_call = made_call.get('type', '')

        if call := self.implemented_calls.get(type_of_call):
            return self._encode(call(made_call))

        raise NotImplementedError('This type of call is not implemented')


    def handle_read(self, call : dict) -> None:
        """ handle a read call
            @param read RPC call 
        """

        if self.required_keys.get('read') - call.keys():
            raise ValueError('Call does not have the required parameters')

        return dict(id=call.get('id'),
                    data=self.read(**call))

    
    def handle_write(self, call : dict) -> None:
        """ handle a write call 
            @param write RPC call
        """

        if self.required_keys.get('write') - call.keys():
            raise ValueError('Call does not have the required parameters')

        return dict(id=call.get('id'),
                    written=self.write(**call))
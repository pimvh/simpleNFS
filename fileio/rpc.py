import json
import uuid

from fileio.local import LocalImpl
from ..servers.tcp_dgram_server import DatagramTCPSocket



class RPCBase:
    def __init__(self, ip, port, process_func) -> None:
        self.socket = DatagramTCPSocket(ip, port, process_func)

        default_keys = {'type', 'id', 'filename', 'offset'}

        self.required_keys = {
            'read'  : default_keys & {'length'},
            'write' : default_keys & {'block'}
        }


    @staticmethod
    def _encode(data : dict) -> hex:
        """ dump the dict as a json, and hex-encode """
        return json.dumps(data).encode('hex')


    @staticmethod
    def _decode(bytes : str) -> dict:
        """ hex-decode and parse the dict from the json """
        return json.load(str(bytes))


    def _send_call(self, call) -> None:
        """ send a RPC over the network """
        self.socket.send(call)


    def _retrieve_reply(self) -> dict:
        """ wait for RP reply """
        data = self.socket.recv()
        return json.loads(str(data))

    
    def _send_reply(self, data) -> None:
        """ send a reply to an RPC over the network """
        self.socket.send(self._encode(data))


class RPCClient(RPCBase):
    """ implementation of an RPC client, depends on
        the RPC base 
    """
    def __init__(self, ip, port) -> None:
        """ @params ip to run on 
            @params port to run on
        """

        super().__init__(ip, port)

    def read(self, **kwargs):
        """ send data to the socket, and decode the reply
             @param filename The file to read from.
             @param offset   The offset to start reading from.
             @param length   The number of bytes to read.
             @return The data read or '' in case of error.
        """

        self._send_call(self._encode(dict(type='read',
                                          id=uuid.uuid4(),
                                          **kwargs)))

        return self._retrieve_reply().get('data', '')


    def write(self, **kwargs):
        """ send the write data to the file
        @param filename The file to write to.
        @param offset   The offset to write at.
        @param block    The block of data to write.
        @return The number of bytes written or -1 in case of error.
        """
        
        self._send_call(self._encode(dict(type='write',
                                          id=uuid.uuid4(),
                                          **kwargs)))

        return self._retrieve_reply().get('data', '')


class RPCServer(RPCBase, LocalImpl):
    """ implementation of an RPC server, depends on the local implementation 
        and the RPC base 
    """
    def __init__(self, ip, port) -> None:
        """ @params ip to run on 
            @params port to run on
        """

        super().__init__(ip, port, self.make_reply())

        self.implemented_calls = {
            'read'  : self.read_reply,
            'write' : self.write_reply,
        }
    
    def run(self) -> None:
        """ start the underlying socket """
        self.socket.run()

    def make_reply(self, made_call : dict) -> None:
        """ figure out what to reply based on incoming TCP data 
            @param the incoming call 
        """

        if not 'call' in made_call:
            return 

        type_of_call = made_call.get('type', '')

        if call := self.implemented_calls.get(type_of_call):
            call(made_call)

        raise NotImplementedError('This type of call is not implemented')


    def handle_read(self, call : dict) -> None:
        """ handle a read call
            @param read RPC call 
        """

        if self.required_keys.get('read') - call:
            raise ValueError('Call does not have the required parameters')

        self._send_reply(dict(id=call.get('id'),
                              data=self.read(**call)))

    
    def handle_write(self, call : dict) -> None:
        """ handle a write call 
            @param write RPC call
        """

        if self.required_keys.get('write') - call:
            raise ValueError('Call does not have the required parameters')

        self._send_reply(dict(id=call.get('id'),
                              data=self.write(**call)))
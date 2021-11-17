import asyncio

async def tcp_echo_client(ip : str, port : int, message : str):
    """ runs a tcp echo client 
        @param ip to run on 
        @message to send 
    """
    reader, writer = await asyncio.open_connection(ip, port)

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
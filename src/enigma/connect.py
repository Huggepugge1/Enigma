import socket

from . import encode


class Connection:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))


    def close(self):
        return self.close()


    def recv(self, bytes: int=1024) -> bytes:
        return self.socket.recv(bytes)


    def recvline(self) -> bytes:
        recieved_string = b""
        while (recieved_byte := self.socket.recv(1)) != b"\n":
            recieved_string += recieved_byte
        
        return recieved_string
    

    def recvuntil(self, string: bytes) -> bytes:
        recieved_string = b""
        while recieved_byte := self.socket.recv(1):
            recieved_string += recieved_byte
            if string in recieved_string:
                break
        
        return recieved_string


    def recvall(self) -> bytes:
        recieved_string = b""
        while recieved_byte := self.socket.recv(1):
            recieved_string += recieved_byte
        
        return recieved_string


    def send(self, string: bytes, end: bytes=b"\n"):
        self.socket.send(string + end)


    def send_and_recv(self, string: bytes, end: bytes=b"\n", recv_size: int=1024):
        self.socket.send(string + end)
        return self.recv(recv_size)


def connect(host, port):
    return Connection(host, port)

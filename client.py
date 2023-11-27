import socket
import threading

class client:
    """Client class for connecting to a server"""
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientID = ""
    clientIP = ""
    clientPort = 0

    def __init__(self, ip:str, port:int, ID = "") -> None:
        """Sets all variables"""
        self.clientIP = ip
        self.clientPort = port
        self.clientID = ID

    def send(self, msg:str) -> None:
        """Sends a message to the server"""
        if msg == "~quit":
            self.clientSocket.close()
            exit()
        package = msg.encode()
        length = len(package)
        self.clientSocket.send(length.to_bytes(4, 'big'))
        self.clientSocket.send(package)

    def receive(self) -> str:
        """Receives a message from the server"""
        length = int.from_bytes(self.clientSocket.recv(4), 'big')
        package = self.clientSocket.recv(length)
        return package.decode()

    def setID(self):
        """Sets the clientID"""
        self.clientID = input("Enter your name: ")

    def listen(self) -> None:
        """Listens for messages from the server"""
        while True:
            msg = self.receive()
            print(msg)    

    def connect(self) -> None:
        """Connects to the server"""
        self.clientSocket.connect((self.clientIP, self.clientPort))
        self.clientSocket.send(len(self.clientID).to_bytes(1, 'big'))
        self.clientSocket.send(self.clientID.encode())
        threading.Thread(target=self.listen, daemon=True).start()


if __name__ == "__main__":
    client = client(input("Enter server IP: "), 1234)
    client.setID()
    client.connect()
    while True:
        msg = input()
        client.send(msg)



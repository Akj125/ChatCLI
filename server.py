import socket
import threading
        
class server:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    clients = []

    def __init__(self, port:int) -> None:
        """Binds to 0.0.0.0 at designated port"""
        self.serverSocket.bind(("0.0.0.0", port))

    def send(self, msg:str, ID:str, sender=None):
        """Send msg to the room"""
        msg = ID + " : " + msg
        package = msg.encode()
        length = len(package)
        for client in self.clients:
            if client == sender:
                continue
            try :
                client.send(length.to_bytes(4, 'big'))
                client.send(package)
            except:
                self.clients.remove(client)
                print("Client disconnected: " + ID)
                self.send("has left the chat", ID, sender=client)

    def listen(self, client:socket, ID) -> None:
        """Listens for messages from a client"""
        while True:
            try:
                length = int.from_bytes(client.recv(4), 'big')
                package = client.recv(length)
                msg = package.decode()
                self.send(msg, ID, sender=client)
            except:
                self.clients.remove(client)
                print("Client disconnected: " + ID)
                self.send("has left the chat", ID, sender=client)
                break

    def connect(self) -> None:
        """Waits for and accepts connections from clients"""
        while True:
            self.serverSocket.listen()
            socket, ip = self.serverSocket.accept()
            size = int.from_bytes(socket.recv(1), 'big')
            clientID = socket.recv(size).decode()
            print("Client connected: " + clientID)
            self.send("has joined the chat", clientID)
            threading.Thread(target=self.listen, args=(socket, clientID)).start()
            self.clients.append(socket)


if __name__ == "__main__":
    server = server(1234)
    threading.Thread(target=server.connect).start()
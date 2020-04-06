from threading import Thread, Lock, Event
import socket
import time


class SocketCommunicator():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('', 10000)
        self.sock.bind(server_address)
        self.sock.listen(1)

        self.theData = []
        self.theDataLock = Lock()
        self.shutdown_event = Event()
        self.theThread = None

        self.connections = []

    def startServer(self):
        if self.theThread is not None:
            return
        def start():
            while not self.shutdown_event.is_set():
                print('waiting for connection...')
                connection, client_address = self.sock.accept()
                print('accepted connection from: {}'.format(client_address))
                data = connection.recv(1)
                if data:
                    data = data.decode()
                    print(data)
                    print()
                    with self.theDataLock:
                        self.theData.append(data)
            self.sock.close()
        servThread = Thread(target=start, daemon=True)
        servThread.start()
        self.theThread = servThread

    def sendMessage(self, addr, port, data):
        connection = socket.create_connection((addr, port))
        connection.sendall(data)
        connection.close()

    def stop(self):
        self.shutdown_event.set()
        if self.theThread is not None:
            self.theThread.join()

    def getTheData(self):
        with self.theDataLock:
            tmp = self.theData.copy()
            self.theData = []
            return tmp


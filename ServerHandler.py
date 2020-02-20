import struct

from IconManager import IconManager
from LogEntry import LogEntry
from LogEntryManager import LogEntryManager
from Vector import Vector
from VectorManager import VectorManager
import socket
import threading
import pickle
from threading import Thread

def synchronized_method(method):
    outer_lock = threading.Lock()
    lock_name = "__" + method.__name__ + "_lock" + "__"

    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name): setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

    return sync_method

class ServerHandler():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 65432
        self.leadAddress = None
        self.bind()
        self.logEntryManager = LogEntryManager()
        self.logEntryManager.retrieveLogEntries()
        self.vectorManager = VectorManager()
        self.vectorManager.retrieveVectors()
        self.iconManager = IconManager()
        self.iconManager.retrieveIcons()
        self.clientsConnected = list()

    def bind(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen()

    def addNewClient(self, clientAddress):
        self.clientsConnected.append(clientAddress)

    def removeClient(self, clientAddress):
        self.clientsConnected.remove(clientAddress)

class ServerThread(Thread):
    def __init__(self, clientSocket, serverHandler):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        self.serverHandler = serverHandler

    def sendMsg(self, msg):
        msg = struct.pack('>I', len(msg)) + msg
        self.clientSocket.sendall(msg)

    def recvMsg(self):
        raw_msglen = self.recvAll(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.recvAll(msglen)

    def recvAll(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.clientSocket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    @synchronized_method
    def handleIconManagerRequest(self):
        self.sendMsg(pickle.dumps(self.serverHandler.iconManager.icons))

    @synchronized_method
    def handleIconManagerUpdate(self, icons):
        for iconName in list(self.serverHandler.iconManager.icons.keys()):
            if iconName not in icons:
                icons[iconName] = self.serverHandler.iconManager.icons[iconName]
        self.serverHandler.iconManager.icons = icons
        self.serverHandler.iconManager.storeIcons()
        self.sendMsg(pickle.dumps(self.serverHandler.iconManager.icons))

    @synchronized_method
    def handleLogEntryUpdate(self, logEntry):
        if self.serverHandler.logEntryManager.updateLogEntry(logEntry):
            self.sendMsg(pickle.dumps(logEntry))
        else:
            self.sendMsg(pickle.dumps(None))

    @synchronized_method
    def handleSetLead(self, address):
        if self.serverHandler.leadAddress == None:
            self.serverHandler.leadAddress = address
            self.sendMsg(pickle.dumps(address))
        else:
            self.sendMsg(pickle.dumps(self.serverHandler.leadAddress))

    @synchronized_method
    def handleReleaseLead(self, address):
        if self.serverHandler.leadAddress == address:
            self.serverHandler.leadAddress = None
            self.sendMsg(pickle.dumps(True))
        else:
            self.sendMsg(pickle.dumps(False))

    def run(self):
        vector = Vector()
        vector.addSignificantEventFromLogEntry(LogEntry())
        msg = pickle.dumps({"Server Information" : {"Lead Address" : self.serverHandler.leadAddress, "Connected Clients" : self.serverHandler.clientsConnected}})
        self.sendMsg(msg)
        while True:
            msg = pickle.loads(self.recvMsg())
            print(msg)
            request = list(msg.keys())[0]
            if request == "Icon Manager Request":
                self.handleIconManagerRequest()
            elif request == "Icon Manager Update":
                self.handleIconManagerUpdate(list(msg.values())[0])
            elif request == "Log Entry Update":
                self.handleLogEntryUpdate(list(msg.values())[0])
            elif request == "Set Lead":
                self.handleSetLead(list(msg.values())[0])

if __name__ == "__main__":
    serverHandler = ServerHandler()
    while True:
        clientSocket, clientAddress = serverHandler.serverSocket.accept()
        serverHandler.addNewClient(clientAddress)
        serverThread = ServerThread(clientSocket, serverHandler)
        serverThread.start()


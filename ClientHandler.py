import struct
import socket
import pickle

from LogEntryManager import LogEntryManager
from VectorManager import VectorManager
from IconManager import IconManager

class ClientHandler():
    def __init__(self):
        self.logEntryManager = LogEntryManager()
        self.vectorManager = VectorManager()
        self.iconManager = IconManager()
        self.isLead = False
        self.leadIp = None
        self.serverIp = '127.0.0.1'
        self.serverPort = 65432
        self.connectionStatus = False
        self.establishedConnections = 0
        self.numConnections = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.serverIp, self.serverPort))
        serverInformation = self.recvMsg()
        serverInformation = pickle.loads(serverInformation)
        serverInformation = list(serverInformation.values())[0]
        self.leadIp = serverInformation["Lead"]
        self.establishedConnections = len(serverInformation["Connected Clients"])
        self.numConnections = self.establishedConnections

    def requestIcons(self):
        self.sendMsg(pickle.dumps({"Icon Manager Request": None}))
        self.iconManager.icons = pickle.loads(self.recvMsg())

    def updateIcons(self):
        self.sendMsg(pickle.dumps({"Icon Manager Update": self.iconManager.icons}))
        self.iconManager.icons = pickle.loads(self.recvMsg())

    def sendMsg(self, msg):
        msg = struct.pack('>I', len(msg)) + msg
        self.socket.sendall(msg)

    def recvMsg(self):
        raw_msglen = self.recvAll(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.recvAll(msglen)

    def recvAll(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def pullVectorDb(self):
        self.vectorManager.pullVectorDb()
        vectors = list(self.vectorManager.vectors.values())
        self.logEntryManager.updateLogEntries(vectors)
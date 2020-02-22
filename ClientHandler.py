import struct
import socket
import pickle
import uuid

from LogEntryManager import LogEntryManager
from VectorManager import VectorManager
from IconManager import IconManager

class ClientHandler():
    def __init__(self):
        self.logEntryManager = LogEntryManager()
        self.vectorManager = VectorManager()
        self.iconManager = IconManager()
        self.isLead = False
        self.hasLead = False
        self.serverIp = '127.0.0.1'
        self.serverPort = 65432
        self.address = hex(uuid.getnode())
        self.establishedConnections = 0
        self.numConnections = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.serverIp, self.serverPort))
        serverInformation = self.recvMsg()
        serverInformation = pickle.loads(serverInformation)
        serverInformation = list(serverInformation.values())[0]
        self.hasLead = serverInformation["Lead Address"] != None
        if self.hasLead:
            if serverInformation["Lead Address"] == self.address:
                self.isLead = True
        self.establishedConnections = len(serverInformation["Connected Clients"])
        self.numConnections = self.establishedConnections

    def requestIcons(self):
        self.sendMsg(pickle.dumps({"Icon Manager Request": None}))
        self.iconManager.icons = pickle.loads(self.recvMsg())

    def updateIcons(self):
        self.sendMsg(pickle.dumps({"Icon Manager Update": self.iconManager.icons}))
        self.iconManager.icons = pickle.loads(self.recvMsg())

    def editLogEntry(self, logEntry):
        self.sendMsg(pickle.dumps({"Log Entry Update": logEntry}))
        logEntry = pickle.loads(self.recvMsg())
        if logEntry != None:
            self.logEntryManager.updateLogEntry(logEntry)

    def setLead(self):
        self.sendMsg(pickle.dumps({"Set Lead": self.address}))
        address = pickle.loads(self.recvMsg())
        if self.address == address:
            self.isLead = True
            self.hasLead = True

    def releaseLead(self):
        self.sendMsg(pickle.dumps({"Release Lead": self.address}))
        completed = pickle.loads(self.recvMsg())
        if completed:
            self.isLead = False
            self.hasLead = False

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

    def editLogEntryVectors(self, logEntry, newVectors):
        oldVectors = logEntry.associatedVectors
        logEntry.associatedVectors = newVectors
        self.vectorManager.handleUpdateToLogEntry(oldVectors, newVectors, logEntry)
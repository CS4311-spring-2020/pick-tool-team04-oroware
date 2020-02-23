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
            self.pullVectorDb()
            self.isLead = True
            self.hasLead = True

    def pushVectorDb(self, vectorManager):
        pushedVectors = list(vectorManager.vectors.values())
        self.sendMsg(pickle.dumps({"Push Vectors" : pushedVectors}))

    def pullVectorDb(self):
        self.sendMsg(pickle.dumps({"Pull Vectors": None}))
        newVectors = pickle.loads(self.recvMsg()).vectors
        for vector in list(self.vectorManager.vectors.values()):
            if vector.vectorName not in newVectors:
                self.logEntryManager.handleVectorDeleted(vector)
        self.vectorManager.vectors = newVectors
        self.vectorManager.storeVectors()
        vectors = list(self.vectorManager.vectors.values())
        self.logEntryManager.updateLogEntries(vectors)

    def approveVector(self, vectorKey, vector):
        if vector.changeSummary == "Deleted":
            if vector.vectorName in self.vectorManager.vectors:
                del self.vectorManager.vectors[vector.vectorName]
                self.logEntryManager.handleVectorDeleted(vector)
        else:
            self.vectorManager[vector.vectorName] = vector
            vectors = list(self.vectorManager.vectors.values())
            self.logEntryManager.updateLogEntries(vectors)
        self.sendMsg(pickle.dumps({"Approve Vector" : [vectorKey, vector]}))
        return self.getPendingVectors()

    def updateVector(self, vector):
        self.sendMsg(pickle.dumps({"Update Vector": vector}))

    def rejectVector(self, vectorKey):
        self.sendMsg(pickle.dumps({"Reject Vector" : vectorKey}))
        return self.getPendingVectors()

    def getPendingVectors(self):
        self.sendMsg(pickle.dumps({"Get Pending Vectors" : None}))
        pendingVectors = pickle.loads(self.recvMsg())
        return pendingVectors

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

    def editLogEntryVectors(self, logEntry, newVectors):
        oldVectors = logEntry.associatedVectors
        logEntry.associatedVectors = newVectors
        self.vectorManager.handleUpdateToLogEntry(oldVectors, newVectors, logEntry)
        if self.isLead:
            for vectorName in oldVectors:
                self.updateVector(self.vectorManager.vectors[vectorName])
            for vectorName in newVectors:
                self.updateVector(self.vectorManager.vectors[vectorName])
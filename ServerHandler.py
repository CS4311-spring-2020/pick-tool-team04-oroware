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
from pathlib import Path

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
        self.logEntryManager = LogEntryManager()
        self.logEntryManager.initPlaceholderData()
        self.logEntryManager.retrieveLogEntries()
        self.vectorManager = VectorManager()
        self.vectorManager.retrieveVectors()
        self.iconManager = IconManager()
        self.iconManager.retrieveIcons()
        self.pendingVectors = dict()
        self.pendingVectorFilename = "pendingVectors.pkl"
        self.retrievePendingVectors()
        self.clientsConnected = list()
        self.bind()

    def bind(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen()

    def addNewClient(self, clientAddress):
        self.clientsConnected.append(clientAddress)

    def removeClient(self, clientAddress):
        self.clientsConnected.remove(clientAddress)

    def storePendingVectors(self):
        with open(self.pendingVectorFilename, 'wb') as pkl_file:
            pickle.dump(self.pendingVectors, pkl_file)

    def retrievePendingVectors(self):
        filename_path = Path(self.pendingVectorFilename)
        if filename_path.exists():
            with open(self.pendingVectorFilename, 'rb') as pkl_file:
                self.pendingVectors = pickle.load(pkl_file)

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

    @synchronized_method
    def handlePushedVectors(self, pushedVectors):
        key = 0 if len(self.serverHandler.pendingVectors.keys()) == 0 else (max(self.serverHandler.pendingVectors.keys()) + 1)
        for vector in pushedVectors:
            self.serverHandler.pendingVectors[key] = vector
        self.serverHandler.storePendingVectors()

    @synchronized_method
    def handlePullVectors(self):
        self.sendMsg(pickle.dumps(self.serverHandler.vectorManager))

    @synchronized_method
    def handleUpdateVector(self, vector):
        self.serverHandler.vectorManager.vectors[vector.vectorName] = vector
        self.serverHandler.vectorManager.storeVectors()
        vectors = list(self.serverHandler.vectorManager.vectors.values())
        self.serverHandler.logEntryManager.updateLogEntries(vectors)

    @synchronized_method
    def handlePendingVectors(self):
        self.sendMsg(pickle.dumps(self.serverHandler.pendingVectors))

    @synchronized_method
    def handleApproveVector(self, vectorKey, vector):
        del self.serverHandler.pendingVectors[vectorKey]
        self.serverHandler.storePendingVectors()
        if vector.changeSummary == "Deleted":
            if vector.vectorName in self.serverHandler.vectorManager.vectors:
                del self.serverHandler.vectorManager.vectors[vector.vectorName]
                self.serverHandler.vectorManager.storeVectors()
                self.serverHandler.logEntryManager.handleVectorDeleted(vector)
        else:
            self.serverHandler.vectorManager.vectors[vector.vectorName] = vector
            self.serverHandler.vectorManager.storeVectors()
            vectors = list(self.serverHandler.vectorManager.vectors.values())
            self.serverHandler.logEntryManager.updateLogEntries(vectors)

    @synchronized_method
    def handleRejectVector(self, vectorKey):
        self.serverHandler.storePendingVectors()
        del self.serverHandler.pendingVectors[vectorKey]

    @synchronized_method
    def handleSendLogEntries(self, logEntries):
        for logEntry in logEntries:
            self.serverHandler.logEntryManager.addLogEntry(logEntry)

    @synchronized_method
    def handleSearchLogs(self, commandSearch, creatorBlueTeam, creatorWhiteTeam, creatorRedTeam, eventTypeBlueTeam, eventTypeWhiteTeam, eventTypeRedTeam, startTime, endTime, locationSearch):
        logEntries = self.serverHandler.logEntryManager.searchLogEntries(commandSearch, creatorBlueTeam, creatorWhiteTeam, creatorRedTeam, eventTypeBlueTeam, eventTypeWhiteTeam, eventTypeRedTeam, startTime, endTime, locationSearch)
        self.sendMsg(pickle.dumps(logEntries))

    def run(self):
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
            elif request == "Release Lead":
                self.handleReleaseLead(list(msg.values())[0])
            elif request == "Push Vectors":
                self.handlePushedVectors(list(msg.values())[0])
            elif request == "Get Pending Vectors":
                self.handlePendingVectors()
            elif request == "Approve Vector":
                vectorTuple = list(msg.values())[0]
                self.handleApproveVector(vectorTuple[0], vectorTuple[1])
            elif request == "Reject Vector":
                self.handleRejectVector(list(msg.values())[0])
            elif request == "Pull Vectors":
                self.handlePullVectors()
            elif request == "Update Vector":
                self.handleUpdateVector(list(msg.values())[0])
            elif request == "Send Log Entries":
                self.handleSendLogEntries(list(msg.values())[0])
            elif request == "Search Logs":
                searchCriteria = list(msg.values())[0]
                commandSearch = searchCriteria[0]
                creatorBlueTeam = searchCriteria[1]
                creatorWhiteTeam = searchCriteria[2]
                creatorRedTeam = searchCriteria[3]
                eventTypeBlueTeam = searchCriteria[4]
                eventTypeWhiteTeam = searchCriteria[5]
                eventTypeRedTeam = searchCriteria[6]
                startTime = searchCriteria[7]
                endTime = searchCriteria[8]
                locationSearch = searchCriteria[9]
                self.handleSearchLogs(commandSearch, creatorBlueTeam, creatorWhiteTeam, creatorRedTeam, eventTypeBlueTeam, eventTypeWhiteTeam, eventTypeRedTeam, startTime, endTime, locationSearch)

if __name__ == "__main__":
    serverHandler = ServerHandler()
    while True:
        clientSocket, clientAddress = serverHandler.serverSocket.accept()
        serverHandler.addNewClient(clientAddress)
        serverThread = ServerThread(clientSocket, serverHandler)
        serverThread.start()


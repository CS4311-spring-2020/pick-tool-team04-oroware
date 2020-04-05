import os
import struct
import socket
import pickle
import threading
import uuid
from pathlib import Path

from EventConfig import EventConfig
from LogEntryManager import LogEntryManager
from LogFileManager import LogFileManager
from VectorManager import VectorManager
from IconManager import IconManager

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


class ClientHandler():
    def __init__(self):
        self.logEntryManager = LogEntryManager()
        self.vectorManager = VectorManager()
        self.vectorManager.retrieveVectors()
        self.iconManager = IconManager()
        self.logFileManager = LogFileManager()
        self.logFileManager.retrieveRootPath()
        self.logFileManager.retrieveLogFilesDb()
        self.eventConfig = EventConfig()
        self.isLead = False
        self.hasLead = False
        self.serverIp = '127.0.0.1'
        self.serverPort = 65433
        self.address = hex(uuid.getnode())
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.serverIp, self.serverPort))
        serverInformation = self.recvMsg()
        serverInformation = pickle.loads(serverInformation)
        serverInformation = list(serverInformation.values())[0]
        self.hasLead = serverInformation["Lead Address"] != None
        if self.hasLead:
            if serverInformation["Lead Address"] == self.address:
                self.isLead = True
        self.requestEventConfig()

    @synchronized_method
    def requestIcons(self):
        self.iconManager.retrieveIconsDb()

    @synchronized_method
    def requestEventConfig(self):
        self.eventConfig.retrieveEventConfigDb()

    @synchronized_method
    def updateEventConfig(self):
        self.eventConfig.storeEventConfigDb()

    @synchronized_method
    def updateIcons(self):
        self.iconManager.updateIconsDb()

    @synchronized_method
    def deleteIcon(self, iconName):
        self.iconManager.deleteIconDb(iconName)

    @synchronized_method
    def editLogEntry(self, logEntry):
        self.logEntryManager.updateLogEntryDb(logEntry)

    @synchronized_method
    def setLead(self):
        self.sendMsg(pickle.dumps({"Set Lead": self.address}))
        self.vectorManager.deleteStoredVectors()
        self.deletePulledVectors()
        self.deletePushedVectors()
        address = pickle.loads(self.recvMsg())
        if self.address == address:
            self.pullVector()
            self.isLead = True
            self.hasLead = True

    @synchronized_method
    def pushVector(self, vectorManager):
        pushedVectors = list(vectorManager.vectors.values())
        self.sendMsg(pickle.dumps({"Push Vectors" : pushedVectors}))

    @synchronized_method
    def pullVector(self):
        self.sendMsg(pickle.dumps({"Pull Vectors": None}))
        newVectors = pickle.loads(self.recvMsg()).vectors
        for vector in list(self.vectorManager.vectors.values()):
            if vector.vectorName not in newVectors:
                self.logEntryManager.handleVectorDeleted(vector)
        self.vectorManager.vectors = newVectors
        self.vectorManager.storeVectors()
        vectors = list(self.vectorManager.vectors.values())
        self.logEntryManager.updateLogEntries(vectors)

    @synchronized_method
    def approveVector(self, vectorKey, vector):
        if vector.changeSummary == "Deleted":
            if vector.vectorName in self.vectorManager.vectors:
                del self.vectorManager.vectors[vector.vectorName]
                self.logEntryManager.handleVectorDeleted(vector)
                self.logEntryManager.handleVectorDeletedDb(vector)
        else:
            self.handleDeletedEvents(vector)
            self.vectorManager.vectors[vector.vectorName] = vector
            vectors = list(self.vectorManager.vectors.values())
            self.logEntryManager.updateLogEntries(vectors)
            self.logEntryManager.updateLogEntriesDb(vectors)
        self.sendMsg(pickle.dumps({"Approve Vector" : [vectorKey, vector]}))
        return self.getPendingVectors()

    @synchronized_method
    def handleDeletedEvents(self, vector):
        originalVector = self.vectorManager.vectors[vector.vectorName]
        updatedLogEntries = set()
        for significantEventId, significantEvent in vector.significantEvents.items():
            updatedLogEntries.add(significantEvent.logEntry.id)
        for significantEventId, significantEvent in originalVector.significantEvents.items():
            if significantEvent.logEntry.id not in updatedLogEntries:
                self.logEntryManager.handleEventDeletedDb(significantEvent.logEntry)

    @synchronized_method
    def updateVector(self, vector):
        self.logEntryManager.updateLogEntries([vector])
        self.logEntryManager.updateLogEntriesDb([vector])
        self.sendMsg(pickle.dumps({"Update Vector": vector}))

    @synchronized_method
    def sendLogEntries(self, logEntries):
        for logEntry in logEntries:
            self.logEntryManager.storeLogEntryDb(logEntry)

    @synchronized_method
    def searchLogEntries(self, commandSearch, creatorBlueTeam, creatorWhiteTeam, creatorRedTeam, eventTypeBlueTeam, eventTypeWhiteTeam, eventTypeRedTeam, startTime, endTime, locationSearch):
        self.logEntryManager.retrieveLogEntriesDb()
        validLogEntries = self.logEntryManager.searchLogEntries(commandSearch, creatorBlueTeam, creatorWhiteTeam, creatorRedTeam, eventTypeBlueTeam, eventTypeWhiteTeam, eventTypeRedTeam, startTime, endTime, locationSearch)
        self.logEntryManager.logEntries.clear()
        self.logEntryManager.logEntriesInTable = validLogEntries
        for logEntry in validLogEntries:
            self.logEntryManager.logEntries[logEntry.id] = logEntry
            currentAssociatedVectors = list()
            for vectorName, vector in self.vectorManager.vectors.items():
                for signficiantEventId, significantEvent in vector.significantEvents.items():
                    if significantEvent.logEntry.id == logEntry.id:
                        currentAssociatedVectors.append(vectorName)
            logEntry.associatedVectors = currentAssociatedVectors

    @synchronized_method
    def rejectVector(self, vectorKey):
        self.sendMsg(pickle.dumps({"Reject Vector" : vectorKey}))
        return self.getPendingVectors()

    @synchronized_method
    def getPendingVectors(self):
        self.sendMsg(pickle.dumps({"Get Pending Vectors" : None}))
        pendingVectors = pickle.loads(self.recvMsg())
        return pendingVectors

    @synchronized_method
    def releaseLead(self):
        self.sendMsg(pickle.dumps({"Release Lead": self.address}))
        completed = pickle.loads(self.recvMsg())
        if completed:
            self.isLead = False
            self.hasLead = False
            for vector in list(self.vectorManager.vectors.values()):
                self.logEntryManager.handleVectorDeleted(vector)
            self.vectorManager.vectors.clear()
            self.vectorManager.deleteStoredVectors()

    @synchronized_method
    def sendMsg(self, msg):
        msg = struct.pack('>I', len(msg)) + msg
        self.socket.sendall(msg)

    @synchronized_method
    def recvMsg(self):
        raw_msglen = self.recvAll(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.recvAll(msglen)

    @synchronized_method
    def recvAll(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    @synchronized_method
    def deletePushedVectors(self):
        filename_path = Path("pushedVectors.pkl")
        if filename_path.exists():
            os.remove(filename_path)

    @synchronized_method
    def deletePulledVectors(self):
        filename_path = Path("pulledVectors.pkl")
        if filename_path.exists():
            os.remove(filename_path)

    @synchronized_method
    def editLogEntryVectors(self, logEntry, newVectors):
        oldVectors = logEntry.associatedVectors
        logEntry.associatedVectors = newVectors
        self.vectorManager.handleUpdateToLogEntry(oldVectors, newVectors, logEntry)
        if self.isLead:
            for vectorName in oldVectors:
                self.updateVector(self.vectorManager.vectors[vectorName])
            for vectorName in newVectors:
                self.updateVector(self.vectorManager.vectors[vectorName])
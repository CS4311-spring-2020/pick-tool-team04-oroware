from LogEntryManager import LogEntryManager
from VectorManager import VectorManager
from IconManager import IconManager

class ClientHandler():
    def __init__(self):
        self.logEntryManager = LogEntryManager()
        self.vectorManager = VectorManager()
        self.iconManager = IconManager()

    def editLogEntryVectors(self, logEntry, newVectors):
        oldVectors = logEntry.associatedVectors
        logEntry.associatedVectors = newVectors
        self.vectorManager.handleUpdateToLogEntry(oldVectors, newVectors, logEntry)

    def pullVectorDb(self):
        self.vectorManager.pullVectorDb()
        vectors = list(self.vectorManager.vectors.values())
        self.logEntryManager.updateLogEntries(vectors)
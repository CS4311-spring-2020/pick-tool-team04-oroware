from Vector import Vector

class VectorManager:
    def __init__(self):
        self.vectors = dict()
        sampleVector = Vector()
        sampleVector.vectorName = "SQL Attack"
        sampleVector.vectorDescription = "SQL Attack by Red Team"
        self.vectors[sampleVector.vectorName] = sampleVector

    def handleUpdateToLogEntry(self, oldVectorNames, newVectorNames, logEntry):
        addedVectorNames = list()
        deletedVectorNames = list()
        updatedVectorNames = list()
        for vectorName in oldVectorNames:
            if vectorName in newVectorNames:
                updatedVectorNames.append(vectorName)
            else:
                deletedVectorNames.append(vectorName)
        for vectorName in newVectorNames:
            if vectorName not in oldVectorNames:
                addedVectorNames.append(vectorName)
        for vectorName in updatedVectorNames:
            if vectorName in self.vectors:
                self.vectors[vectorName].updateLogEntry(logEntry)
        for vectorName in addedVectorNames:
            if vectorName in self.vectors:
                self.vectors[vectorName].addSignificantEventFromLogEntry(logEntry)
        for vectorName in deletedVectorNames:
            if vectorName in self.vectors:
                self.vectors[vectorName].removeSignificantEventByLogEntryId(logEntry.id)



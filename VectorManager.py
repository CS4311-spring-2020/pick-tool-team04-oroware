import pickle

from LogEntry import LogEntry
from Vector import Vector
from pathlib import Path

class VectorManager:
    def __init__(self):
        self.vectors = dict()
        self.filename = "vectors.pkl"
        self.logEntryManager = None

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

    def pullVectorDb(self):
        pulledVector1 = Vector()
        pulledVector1.vectorName = "SQL Attack"
        pulledVector1.vectorDescription = "SQL Attack by Red Team"
        self.vectors[pulledVector1.vectorName] = pulledVector1
        pulledVector2 = Vector()
        pulledVector2.vectorName = "SQL Defense"
        pulledVector2.vectorDescription = "SQL Defense by Blue Team"
        ids = [0, 1]
        dates = ["1/31/2020 12:08 AM", "2/1/2020 11:43 PM"]
        teams = [LogEntry.BLUE_TEAM, LogEntry.WHITE_TEAM]
        descriptions = ["Blue Team Defender Turns on Computer.", "White Team Analyst Starts Taking Notes."]
        artifacts = ["blue_log.csv", "white_recording.png"]
        for i in range(len(ids)):
            logEntry = LogEntry()
            logEntry.date = dates[i]
            logEntry.description = descriptions[i]
            logEntry.creator = teams[i]
            logEntry.eventType = teams[i]
            logEntry.id = ids[i]
            logEntry.artifact = artifacts[i]
            pulledVector2.addSignificantEventFromLogEntry(logEntry)
        pulledVector2.addNewRelationship(0, 1)
        pulledVector2.visibility["Artifact"] = True
        for relationship in list(pulledVector2.relationships.values()):
            relationship.label = "causes"
        self.vectors[pulledVector2.vectorName] = pulledVector2

    def addVector(self, vector):
        if vector.vectorName in self.vectors:
            return False
        self.vectors[vector.vectorName] = vector
        print()
        return True

    def deleteVector(self, vector):
        if vector.vectorName in self.vectors:
            self.vectors[vector.vectorName] = None
            return True
        else:
            return False

    def storeVectors(self):
        with open(self.filename, 'wb') as pkl_file:
            pickle.dump(self.vectors, pkl_file)

    def retrieveVectors(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            with open(self.filename, 'rb') as pkl_file:
                self.vectors = pickle.load(pkl_file)




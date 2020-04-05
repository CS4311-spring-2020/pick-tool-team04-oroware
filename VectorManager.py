import os
import pickle
from pathlib import Path

import pymongo


class VectorManager:
    def __init__(self):
        self.vectors = dict()
        self.filename = "vectors.pkl"

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

    def addVector(self, vector):
        if vector.vectorName in self.vectors:
            return False
        self.vectors[vector.vectorName] = vector
        return True

    def deleteVector(self, vectorName):
        if vectorName in self.vectors:
            del self.vectors[vectorName]
            self.storeVectors()
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

    def deleteStoredVectors(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            os.remove(filename_path)



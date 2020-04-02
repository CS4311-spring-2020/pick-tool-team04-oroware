import os
import pickle
from pathlib import Path

import pymongo


class VectorManager:
    def __init__(self, address):
        self.vectors = dict()
        self.address = address
        self.filename = "vectors.pkl"
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client["database"]
        self.col = self.db[self.address + "vectors"]

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

    def retrievePushedVectors(self):
        pushedVectorManager = VectorManager(self.address)
        pushedVectorManager.col = pushedVectorManager.db["pushedVectors"]
        pushedVectorManager.retrieveVectorsDb()
        return pushedVectorManager

    def retrievePulledVectors(self):
        pulledVectorManager = VectorManager(self.address)
        pulledVectorManager.col = pulledVectorManager.db["pulledVectors"]
        pulledVectorManager.retrieveVectorsDb()
        return pulledVectorManager

    def retrievePendingVectors(self):
        pendingVectorManager = VectorManager(self.address)
        pendingVectorManager.col = pendingVectorManager.db["pendingVectors"]
        pendingVectorManager.retrieveVectorsDb()
        return pendingVectorManager.vectors

    def storeVectorDb(self, vector):
        vectorEntry = {"_id": vector.vectorName, "vector": pickle.dumps(vector)}
        self.col.insert_one(vectorEntry)

    def pushVectors(self):
        self.col = self.db["pendingVectors"]
        self.storeVectorsDb()
        self.col = self.db["pushedVectors"]
        self.deleteStoredVectorsDb()
        self.storeVectorsDb()
        self.col = self.db[self.address + "vectors"]

    def pullVectors(self):
        self.col = self.db["vectors"]
        self.retrieveVectorsDb()
        self.col = self.db["pulledVectors"]
        self.deleteStoredVectorsDb()
        self.storeVectorsDb()
        self.col = self.db[self.address + "vectors"]
        self.deleteStoredVectorsDb()
        self.storeVectorsDb()

    def retrieveVectorsDb(self):
        self.vectors.clear()
        for fileEntry in self.col.find():
            vector = pickle.loads(fileEntry["vector"])
            self.vectors[vector.vectorName] = vector

    def deleteStoredVectorsDb(self):
        self.col.delete_many({})

    def storeVectorsDb(self):
        for vectorName, vector in self.vectors.items():
            self.storeVectorDb(vector)

    def updateVectorDb(self, vector):
        query = {"_id": vector.vectorName}
        values = {"$set": {"_id": vector.vectorName, "logFile": pickle.dumps(vector)}}
        self.col.update_one(query, values)


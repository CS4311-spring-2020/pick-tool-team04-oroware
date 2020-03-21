import pickle
import re
from datetime import datetime
import pymongo
from pathlib import Path

from LogEntry import LogEntry


class LogEntryManager:
    def __init__(self):
        self.logEntries = dict()
        self.logEntriesInTable = list()
        self.filename = "logEntries.pkl"
        self.nextAvailableId = 0
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client["database"]
        self.col = self.db["entries"]

    def addLogEntry(self, logEntry):
        logEntry.id = self.nextAvailableId
        self.logEntries[self.nextAvailableId] = logEntry
        self.nextAvailableId += 1
        self.storeLogEntryDb(logEntry)

    def updateLogEntries(self, vectors):
        for vector in vectors:
            for significantEvent in list(vector.significantEvents.values()):
                if significantEvent.logEntry.id in self.logEntries:
                    self.logEntries[significantEvent.logEntry.id].associatedVectors.append(vector.vectorName)
                    self.updateLogEntryDb(self.logEntries[significantEvent.logEntry.id])

    def handleVectorDeleted(self, vector):
        for significantEvent in list(vector.significantEvents.values()):
            if significantEvent.logEntry.id in self.logEntries:
                if vector.vectorName in self.logEntries[significantEvent.logEntry.id].associatedVectors:
                    self.logEntries[significantEvent.logEntry.id].associatedVectors.remove(vector.vectorName)
                    self.updateLogEntryDb(self.logEntries[significantEvent.logEntry.id])

    def storeLogEntries(self):
        with open(self.filename, 'wb') as pkl_file:
            pickle.dump(self.logEntries, pkl_file)

    def storeLogEntryDb(self, logEntry):
        entry = {"_id": str(logEntry.id), "vectors": str(logEntry.associatedVectors), "location": logEntry.location, "eventType": logEntry.eventType, "description": logEntry.description, "creator": logEntry.creator, "date": logEntry.date, "artifact": logEntry.artifact}
        self.col.insert_one(entry)

    def storeLogEntriesDb(self):
        for logEntryId, logEntry in self.logEntries.items():
            self.storeLogEntryDb(logEntry)

    def retrieveLogEntriesDb(self):
        self.logEntries.clear()
        for entry in self.col.find():
            logEntry = LogEntry()
            logEntry.id = int(entry["_id"])
            logEntry.associatedVectors = eval(entry["vectors"])
            logEntry.location = entry["location"]
            logEntry.eventType = entry["eventType"]
            logEntry.description = entry["description"]
            logEntry.creator = entry["creator"]
            logEntry.date = entry["date"]
            logEntry.artifact = entry["artifact"]
            self.logEntries[logEntry.id] = logEntry

    def updateLogEntryDb(self, logEntry):
        query = {"_id": str(logEntry.id)}
        values = {"$set": {"_id": str(logEntry.id), "vectors": str(logEntry.associatedVectors),
                           "location": logEntry.location, "eventType": logEntry.eventType,
                           "description": logEntry.description, "creator": logEntry.creator, "date": logEntry.date,
                           "artifact": logEntry.artifact}}
        self.col.update_one(query, values)

    def updateLogEntriesDb(self, logEntries):
        for logEntry in logEntries:
            self.updateLogEntryDb(logEntry)

    def deleteLogEntriesDb(self):
        self.col.delete_many({})

    def retrieveLogEntries(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            with open(self.filename, 'rb') as pkl_file:
                self.logEntries = pickle.load(pkl_file)

    def updateLogEntry(self, logEntry):
        if logEntry.id in self.logEntries:
            self.logEntries[logEntry.id] = logEntry
            self.updateLogEntryDb(logEntry)
            return True
        return False

    def searchLogEntries(self, commandSearch, creatorBlueTeam, creatorWhiteTeam, creatorRedTeam, eventTypeBlueTeam, eventTypeWhiteTeam, eventTypeRedTeam, startTime, endTime, locationSearch):
        validLogEntries = list()
        for logEntryId, logEntry in self.logEntries.items():
            valid = True
            if not self.validWithCommandSearch(commandSearch, logEntry.description):
                valid = False
            if creatorBlueTeam and ("Blue" not in logEntry.creator):
                valid = False
            if creatorWhiteTeam and ("White" not in logEntry.creator):
                valid = False
            if creatorRedTeam and ("Red" not in logEntry.creator):
                valid = False
            if eventTypeBlueTeam and ("Blue" not in logEntry.eventType):
                valid = False
            if eventTypeWhiteTeam and ("White" not in logEntry.eventType):
                valid = False
            if eventTypeRedTeam and ("Red" not in logEntry.eventType):
                valid = False
            if locationSearch not in logEntry.location:
                valid = False
            if datetime.strptime(logEntry.date, "%m/%d/%Y %I:%M %p") < datetime.strptime(startTime, "%m/%d/%Y %I:%M %p") or datetime.strptime(logEntry.date, "%m/%d/%Y %I:%M %p") > datetime.strptime(endTime, "%m/%d/%Y %I:%M %p"):
                valid = False
            if valid:
                validLogEntries.append(logEntry)
        return validLogEntries

    def validWithCommandSearch(self, commandSearch, description):
        mandatoryCommandSearchList = re.split("AND", commandSearch)
        for search in mandatoryCommandSearchList:
            searchList = re.split("OR", search)
            valid = False
            for subsearch in searchList:
                subsearch = subsearch.strip()
                if re.search(subsearch, description):
                    valid = True
            if not valid:
                return False
        return True
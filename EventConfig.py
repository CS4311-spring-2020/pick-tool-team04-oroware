import pickle
from pathlib import Path

import pymongo


class EventConfig():

    def __init__(self):
        super(EventConfig, self).__init__()
        self.eventName = None
        self.eventDescription = None
        self.eventStartTime = None
        self.eventEndTime = None
        self.filename = "eventconfig.pkl"
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client["database"]
        self.col = self.db["config"]

    def storeEventConfig(self):
        with open(self.filename, 'wb') as pkl_file:
            pickle.dump([self.eventName, self.eventDescription, self.eventStartTime, self.eventEndTime], pkl_file)

    def storeEventConfigDb(self):
        configEntry = {"_id": "id", "config": str([self.eventName, self.eventDescription, self.eventStartTime, self.eventEndTime])}
        if self.col.find_one({}):
            query = {"_id": "id"}
            values = {"$set": {"_id": "id", "config": str([self.eventName, self.eventDescription, self.eventStartTime, self.eventEndTime])}}
            self.col.update_one(query, values)
        else:
            self.col.insert_one(configEntry)

    def retrieveEventConfigDb(self):
        if self.col.find_one({}):
            configEntry = self.col.find_one({})
            configFields = eval(configEntry["config"])
            self.eventName = configFields[0]
            self.eventDescription = configFields[1]
            self.eventStartTime = configFields[2]
            self.eventEndTime = configFields[3]

    def deleteEventConfig(self):
        self.col.delete_one({})

    def retrieveEventConfig(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            with open(self.filename, 'rb') as pkl_file:
                eventInformation = pickle.load(pkl_file)
                self.eventName = eventInformation[0]
                self.eventDescription = eventInformation[1]
                self.eventStartTime = eventInformation[2]
                self.eventEndTime = eventInformation[3]
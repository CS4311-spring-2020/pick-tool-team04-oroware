import pickle
from pathlib import Path


class EventConfig():

    def __init__(self):
        super(EventConfig, self).__init__()
        self.eventName = None
        self.eventDescription = None
        self.eventStartTime = None
        self.eventEndTime = None
        self.filename = "eventconfig.pkl"

    def storeEventConfig(self):
        with open(self.filename, 'wb') as pkl_file:
            pickle.dump([self.eventName, self.eventDescription, self.eventStartTime, self.eventEndTime], pkl_file)

    def retrieveEventConfig(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            with open(self.filename, 'rb') as pkl_file:
                eventInformation = pickle.load(pkl_file)
                self.eventName = eventInformation[0]
                self.eventDescription = eventInformation[1]
                self.eventStartTime = eventInformation[2]
                self.eventEndTime = eventInformation[3]
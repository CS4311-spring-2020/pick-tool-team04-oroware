import pickle
from pathlib import Path


class LogFileManager:
    def __init__(self):
        self.files = dict()
        self.filename = "logfiles.pkl"

    def addLogFile(self, logFile):
        if logFile.filename in self.files:
            return False
        self.files[logFile.filename] = logFile
        return True

    def storeLogFiles(self):
        with open(self.filename, 'wb') as pkl_file:
            pickle.dump(self.files, pkl_file)

    def retrieveLogFiles(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            with open(self.filename, 'rb') as pkl_file:
                self.files = pickle.load(pkl_file)
import pickle
from pathlib import Path

import pymongo

from AudioLogFile import AudioLogFile
from ImageLogFile import ImageLogFile
from LogFile import LogFile
from PDFLogFile import PDFLogFile
from SplunkInterface import SplunkInterface
from VideoLogFile import VideoLogFile


class LogFileManager:
    def __init__(self):
        self.files = dict()
        self.filename = "logfiles.pkl"
        self.rootPathFilename = "rootPath.pkl"
        self.splunkInterface = SplunkInterface()
        self.rootPath = None
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client["database"]
        self.col = self.db["files"]

    def addLogFile(self, logFile):
        if logFile.filename in self.files:
            return False
        self.files[logFile.filename] = logFile
        return True

    def createLogFile(self, filename, creator, eventType):
        logFile = None

        if ".pdf" in filename:
            logFile = PDFLogFile()
        elif ".mp4" in filename:
            logFile = VideoLogFile()
        elif ".mp3" in filename or ".wav" in filename:
            logFile = AudioLogFile()
        elif ".tiff" in filename or ".PNG" in filename or ".JPG" in filename:
            logFile = ImageLogFile()
        else:
            logFile = LogFile(self.splunkInterface)
        if logFile != None:
            logFile.creator = creator
            logFile.filename = filename
            logFile.eventType = eventType
            self.addLogFile(logFile)
            return True

        return False

    def storeLogFileDb(self, logFile):
        fileEntry = {"_id": logFile.filename, "logFile": pickle.dumps(logFile)}
        self.col.insert_one(fileEntry)

    def retrieveLogFilesDb(self):
        self.files.clear()
        for fileEntry in self.col.find():
            logFile = pickle.loads(fileEntry["logFile"])
            self.files[logFile.filename] = logFile

    def deleteLogFilesDb(self):
        self.col.delete_many({})

    def storeLogFilesDb(self):
        for filename, logFile in self.files.items():
            self.storeLogFileDb(logFile)

    def updateLogFileDb(self, logFile):
        query = {"_id": logFile.filename}
        values = {"$set": {"_id": logFile.filename, "logFile": pickle.dumps(logFile)}}
        self.col.update_one(query, values)

    def storeLogFiles(self):
        with open(self.filename, 'wb') as pkl_file:
            pickle.dump([self.files, self.rootPath], pkl_file)

    def storeRootPath(self):
        with open(self.rootPathFilename, 'wb') as pkl_file:
            pickle.dump(self.rootPath, pkl_file)

    def retrieveRootPath(self):
        filename_path = Path(self.rootPathFilename)
        if filename_path.exists():
            with open(self.rootPathFilename, 'rb') as pkl_file:
                self.rootPath = pickle.load(pkl_file)

    def retrieveLogFiles(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            with open(self.filename, 'rb') as pkl_file:
                output = pickle.load(pkl_file)
                self.files = output[0]
                self.rootPath = output[1]
import pickle
from pathlib import Path
from random import randint

from AudioLogFile import AudioLogFile
from ImageLogFile import ImageLogFile
from LogFile import LogFile
from PDFLogFile import PDFLogFile
from VideoLogFile import VideoLogFile


class LogFileManager:
    def __init__(self):
        self.files = dict()
        self.filename = "logfiles.pkl"

    def addLogFile(self, logFile):
        if logFile.filename in self.files:
            return False
        self.files[logFile.filename] = logFile
        return True

    def createLogFile(self, filename, creator, eventType):
        logFile = None

        if ".csv" in filename or ".txt" in filename or ".tmux" in filename:
            logFile = LogFile()
        elif ".pdf" in filename:
            logFile = PDFLogFile()
        elif ".mp4" in filename:
            logFile = VideoLogFile()
        elif ".mp3" in filename or ".wav" in filename:
            logFile = AudioLogFile()
        elif ".tiff" in filename or ".PNG" in filename or ".JPG" in filename:
            logFile = ImageLogFile()
        if logFile != None:
            logFile.creator = creator
            logFile.filename = filename
            logFile.eventType = eventType
            self.addLogFile(logFile)
            return True

        return False


    def storeLogFiles(self):
        with open(self.filename, 'wb') as pkl_file:
            pickle.dump(self.files, pkl_file)

    def retrieveLogFiles(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            with open(self.filename, 'rb') as pkl_file:
                self.files = pickle.load(pkl_file)
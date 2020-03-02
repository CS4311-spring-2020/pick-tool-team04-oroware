import pickle
from pathlib import Path
from random import randint

from AudioLogFile import AudioLogFile
from ImageLogFile import ImageLogFile
from LogFile import LogFile
from VideoLogFile import VideoLogFile


class LogFileManager:
    def __init__(self):
        self.files = dict()
        self.filename = "logfiles.pkl"

        # Hardcoded Log File Attributes
        filenames = ["SampleLogFile1.txt", "SampleLogFile2.csv", "SampleLogFile3.png", "SampleLogFile4.mp4"]
        sources = ["/folders/sampledir/red", "/folders/sampledir/blue", "/folders/sampledir/red",
                    "/folders/sampledir/blue"]
        is_cleansed = [False, True, True, False]
        is_validated = ["Validated", "Not Validated", "Invalid", "Validated"]
        is_ingested = [False, False, False, False]
        is_acknowledged = [False, False, False, False]
        sample_error_msg = "ERROR: This a sample error message!"

        # Inserting sample files into self.files
        for i in range(len(filenames)):
            logFile = LogFile()
            logFile.filename = filenames[i]
            logFile.source = sources[i]
            logFile.cleansed = is_cleansed[i]
            logFile.validated = is_validated[i]
            logFile.ingested = is_ingested[i]
            logFile.invalidLineNumber = randint(0, 1000)
            logFile.errorMessage = sample_error_msg
            self.files[filenames[i]] = logFile

    def addLogFile(self, logFile):
        if logFile.filename in self.files:
            return False
        self.files[logFile.filename] = logFile
        return True

    def createLogFile(self, filename, creator):
        logFile = None

        if ".csv" in filename or ".txt" in filename or ".tmux" in filename:
            logFile = LogFile()
        elif ".mp4" in filename:
            logFile = VideoLogFile()
        elif ".mp3" in filename or ".wav" in filename:
            logFile = AudioLogFile()
        elif ".tiff" in filename or ".png" in filename or ".jpeg" in filename:
            logFile = ImageLogFile()

        if logFile != None:
            logFile.creator = creator
            logFile.filename = filename
            #logFile.eventType = eventType
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
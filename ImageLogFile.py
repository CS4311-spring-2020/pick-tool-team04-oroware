import os
import time

from datetime import datetime

from LogEntry import LogEntry
from LogFile import LogFile
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

class ImageLogFile(LogFile):

    def __init__(self):
        super(ImageLogFile, self).__init__()
        self.cmd = "libraries/tesseract.exe"

    def readLogFile(self):
        pytesseract.pytesseract.tesseract_cmd = self.cmd
        self.lines = list()
        self.lines.append(pytesseract.image_to_string(Image.open(self.filename)))

    def validateLogFile(self, eventStartTime, eventEndTime):
        if not self.cleansed:
            return False
        date = datetime.strptime(time.ctime(os.path.getctime(self.filename)), "%a %b %d %H:%M:%S %Y")
        date = date.strftime("%m/%d/%Y %I:%M %p")
        if date[0] == "0":
            date = date[1:]
        firstHalf = date[:date.index(" ") + 1]
        secondHalf = date[date.index(" ") + 1:]
        if secondHalf[0] == "0":
            secondHalf = secondHalf[1:]
        date = firstHalf + secondHalf
        if datetime.strptime(date, "%m/%d/%Y %I:%M %p") < datetime.strptime(eventStartTime,
                                                                            "%m/%d/%Y %I:%M %p") or datetime.strptime(
                date, "%m/%d/%Y %I:%M %p") > datetime.strptime(eventEndTime, "%m/%d/%Y %I:%M %p"):
            self.invalidLine = "Whole File"
            self.invalidLineNumber = -1
            self.errorMessage = "Invalid date."
            return False
        self.validated = True
        return True

    def ingestLogFile(self):
        if self.validated and not self.ingested:
            logEntries = list()
            date = datetime.strptime(time.ctime(os.path.getctime(self.filename)), "%a %b %d %H:%M:%S %Y")
            date = date.strftime("%m/%d/%Y %I:%M %p")
            if date[0] == "0":
                date = date[1:]
            firstHalf = date[:date.index(" ") + 1]
            secondHalf = date[date.index(" ") + 1:]
            if secondHalf[0] == "0":
                secondHalf = secondHalf[1:]
            date = firstHalf + secondHalf
            lineNumber = 0
            for line in self.lines:
                logEntry = LogEntry()
                logEntry.date = date
                logEntry.description = line
                logEntry.creator = self.creator
                logEntry.eventType = self.eventType
                logEntry.artifact = self.filename
                logEntry.lineNumber = lineNumber
                logEntry.id = logEntry.artifact + "_" + str(logEntry.lineNumber)
                lineNumber += 1
                logEntries.append(logEntry)
            self.ingested = True
            return logEntries
        return None



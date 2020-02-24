import os
import time
import PyPDF2

from datetime import datetime

from LogEntry import LogEntry
from LogFile import LogFile


class PDFLogFile(LogFile):

    def __init__(self):
        super(PDFLogFile, self).__init__()

    def readLogFile(self):
        pdfFileObj = open(self.filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        line = ""

        for pageNumber in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNumber)
            line = line + pageObj.extractText()

        pdfFileObj.close()
        self.lines.append(line)

    def cleanseLogFile(self):
        try:
            self.readLogFile()
            self.cleansed = True
            return True
        except Exception as e:
            print(e)
            return False

    def validateLogFile(self, eventStartTime, eventEndTime):
        if not self.cleansed:
            return False
        date = datetime.strptime(time.ctime(os.path.getctime(self.filename)), "%a %b %d %H:%M:%S %Y")
        date = date.strftime("%m/%d/%Y %H:%M %p")
        if date < eventStartTime or date > eventEndTime:
            self.invalidLine = "Whole File"
            self.invalidLineNumber = -1
            self.errorMessage = "Invalid date."
            return False
        self.validated = True
        return True

    def ingestLogFile(self, creator, eventType):
        if self.validated:
            logEntries = list()
            date = datetime.strptime(time.ctime(os.path.getctime(self.filename)), "%a %b %d %H:%M:%S %Y")
            date = date.strftime("%m/%d/%Y %H:%M %p")
            for line in self.lines:
                logEntry = LogEntry()
                logEntry.date = date
                logEntry.description = line
                logEntry.creator = creator
                logEntry.eventType = eventType
                logEntry.artifact = self.filename
                self.logEntries.append(logEntry)
            self.ingested = True
            return logEntries
        return None



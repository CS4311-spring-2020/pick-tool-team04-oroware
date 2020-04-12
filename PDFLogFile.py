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

        line = line.replace("\n", "")
        line = line.strip()

        pdfFileObj.close()
        self.lines = list()
        self.lines.append(line)

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
        if datetime.strptime(date, "%m/%d/%Y %I:%M %p") < datetime.strptime(eventStartTime, "%m/%d/%Y %I:%M %p") or datetime.strptime(date, "%m/%d/%Y %I:%M %p") > datetime.strptime(eventEndTime, "%m/%d/%Y %I:%M %p"):
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
                logEntries.append(logEntry)
                lineNumber += 1
            self.ingested = True
            return logEntries
        return None



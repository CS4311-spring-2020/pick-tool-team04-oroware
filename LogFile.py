import re
from copy import deepcopy

from LogEntry import LogEntry


class LogFile:

    def __init__(self):
        self.filename = None
        self.cleansed = False
        self.validated = False
        self.ingested = False
        self.invalidLine = None
        self.invalidLineNumber = None
        self.errorMessage = None
        self.lines = list()
        self.logEntries = list()

    def readLogFile(self):
        with open(self.filename) as file_pointer:
            for line in file_pointer:
                self.lines.append(line)

    def cleanseLogFile(self):
        try:
            self.readLogFile()
            index = 0
            for line in deepcopy(self.lines):
                if len(line) == 0:
                    self.lines.remove(0)
                index += 1
            self.cleansed = True
            return True
        except:
            return False

    def validateLogFile(self, eventStartTime, eventEndTime):
        if not self.cleansed:
            return False
        dateRegex = re.compile(r'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} [A,P]M')
        lineNumber = 0
        for line in self.lines:
            if not dateRegex.search(line):
                self.invalidLine = line
                self.invalidLineNumber = lineNumber
                self.errorMessage = "No date."
                return False
            date = re.findall(dateRegex, line)[0]
            if date < eventStartTime or date > eventEndTime:
                self.invalidLine = line
                self.invalidLineNumber = lineNumber
                self.errorMessage = "Invalid date."
                return False
            lineNumber += 1
        self.validated = True
        return True

    def ingestLogFile(self, creator, eventType):
        if self.validated:
            logEntries = list()
            dateRegex = re.compile(r'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} [A,P]M')
            for line in self.lines:
                date = re.findall(dateRegex, line)[0]
                logEntry = LogEntry()
                logEntry.date = date
                logEntry.description = line.replace(date, "").strip()
                logEntry.creator = creator
                logEntry.eventType = eventType
                logEntry.artifact = self.filename
                self.logEntries.append(logEntry)
            self.ingested = True
            return logEntries
        return None


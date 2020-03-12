from datetime import datetime
import re
from copy import deepcopy

from LogEntry import LogEntry


class LogFile:

    def __init__(self, splunkInterface=None):
        self.filename = None
        self.source = None
        self.cleansed = False
        self.validated = None
        self.ingested = False
        self.acknowledged = False # optional, according to SRS
        self.invalidLineNumber = None
        self.errorMessage = None
        self.invalidLine = None
        self.creator = None
        self.eventType = None
        self.splunkInterface = splunkInterface
        self.lines = list()

    def readLogFile(self):
        print(self.filename)
        self.splunkInterface.ingestLogFiles(self.filename)
        self.lines = self.splunkInterface.retrieveLogEntries(self.filename)

    def cleanseLogFile(self):
        try:
            self.readLogFile()
            index = 0
            for line in deepcopy(self.lines):
                if len(line) == 0:
                    self.lines.remove(index)
                index += 1
            self.cleansed = True
            return True
        except Exception as e:
            print(e)
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
            if datetime.strptime(date, "%m/%d/%Y %I:%M %p") < datetime.strptime(eventStartTime,
                                                                                "%m/%d/%Y %I:%M %p") or datetime.strptime(
                    date, "%m/%d/%Y %I:%M %p") > datetime.strptime(eventEndTime, "%m/%d/%Y %I:%M %p"):
                self.invalidLine = line
                self.invalidLineNumber = lineNumber
                self.errorMessage = "Invalid date."
                return False
            lineNumber += 1
        self.validated = True
        return True

    def ingestLogFile(self):
        if self.validated and not self.ingested:
            logEntries = list()
            dateRegex = re.compile(r'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} [A,P]M')
            for line in self.lines:
                date = re.findall(dateRegex, line)[0]
                logEntry = LogEntry()
                logEntry.date = date
                logEntry.description = line.replace(date, "").strip()
                logEntry.creator = self.creator
                logEntry.eventType = self.eventType
                logEntry.artifact = self.filename
                logEntries.append(logEntry)
            self.ingested = True
            return logEntries
        return None


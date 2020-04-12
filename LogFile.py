from datetime import datetime
import unicodedata, re
from copy import deepcopy
import string

from LogEntry import LogEntry


class LogFile:

    def __init__(self, splunkInterface=None):
        self.filename = None
        self.source = None
        self.cleansed = False
        self.validated = False
        self.ingested = False
        self.acknowledged = False # optional, according to SRS
        self.invalidLineNumber = None
        self.errorMessage = None
        self.invalidLine = None
        self.creator = None
        self.eventType = None
        self.splunkInterface = splunkInterface
        self.lines = list()
        self.timestamps = list()

    def cleanLine(self, line):
        control_chars = ''.join(map(chr, list(range(0, 32)) + list(range(127, 160))))
        control_char_re = re.compile('[%s]' % re.escape(control_chars))
        return control_char_re.sub('', line)

    def cleanFile(self, filename):
        lines = list()
        with open(filename, "r") as file_object:
            for line in file_object:
                lines.append(line)
        with open(filename, "w") as file_object:
            for line in lines:
                file_object.write(self.cleanLine(line))
                file_object.write("\n")

    def isIngestable(self):
        self.splunkInterface.ingestLogFiles(self.filename)
        self.splunkInterface.retrieveLogEntries(self.filename)
        return True

    def readLogFile(self):
        self.cleanFile(self.filename)
        self.splunkInterface.ingestLogFiles(self.filename)
        self.lines, self.timestamps = self.splunkInterface.retrieveLogEntries(self.filename)

    def cleanseLogFile(self):
        try:
            self.readLogFile()
            emptyLineIndexes = list()
            for i in range(len(self.lines)):
                if len(self.lines[i]) == 0:
                    emptyLineIndexes.append(i)
            for index in emptyLineIndexes:
                self.lines.remove(index)
            self.cleansed = True
            return True
        except Exception as e:
            print(e)
            return False

    def validateLogFile(self, eventStartTime, eventEndTime):
        if not self.cleansed:
            return False
        lineNumber = 0
        for line in self.lines:
            timestamp = self.timestamps[lineNumber]
            if datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") < datetime.strptime(eventStartTime, "%m/%d/%Y %I:%M %p") or datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") > datetime.strptime(eventEndTime, "%m/%d/%Y %I:%M %p"):
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
            lineNumber = 0
            for line in self.lines:
                logEntry = LogEntry()
                timestamp = self.timestamps[lineNumber]
                timestampAsDate = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                formattedDate = timestampAsDate.strftime("%m/%d/%Y %I:%M %p")
                logEntry.date = formattedDate
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


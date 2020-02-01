from LogEntry import LogEntry
from PyQt5 import QtCore, QtWidgets

class LogEntryManager:
    def __init__(self):
        self.logEntries = dict()
        self.logEntriesInTable = list()
        self.vectorManager = None
        self.nextAvailableId = 5
        ids = [0, 1, 2, 3, 4]
        dates = ["1/31/2020 12:08 AM", "2/1/2020 11:43 PM", "2/2/2020 11:24 PM", "2/3/2020 11:01 AM", "2/4/2020 12:33 PM"]
        teams = [LogEntry.BLUE_TEAM, LogEntry.WHITE_TEAM, LogEntry.RED_TEAM, LogEntry.RED_TEAM, LogEntry.BLUE_TEAM]
        descriptions = ["Blue Team Defender Turns on Computer.", "White Team Analyst Starts Taking Notes.",
                        "SQL Injection attack from Red Team.", "Cross-Site Scripting Attack from Red Team.",
                        "Blue Team Defender turns off computer."]
        artifacts = ["blue_log.csv", "white_recording.png", "red_attack.txt", "red_escalation.txt", "blue_response.csv"]
        for i in range(len(descriptions)):
            logEntry = LogEntry()
            logEntry.date = dates[i]
            logEntry.description = descriptions[i]
            logEntry.creator = teams[i]
            logEntry.eventType = teams[i]
            logEntry.id = ids[i]
            logEntry.artifact = artifacts[i]
            self.logEntries[ids[i]] = logEntry
        self.logEntriesInTable = list(self.logEntries.values())

    def editLogEntryVectors(self, logEntry, newVectors):
        oldVectors = logEntry.associatedVectors
        logEntry.associatedVectors = newVectors
        self.vectorManager.handleUpdateToLogEntry(oldVectors, newVectors, logEntry)



from LogEntry import LogEntry
from PyQt5 import QtCore, QtWidgets

class LogEntryManager:
    def __init__(self):
        self.logEntries = dict()
        self.logEntriesInTable = list()
        self.searchLogEntryTableWidget = None
        self.colNamesInSearchLogsTable = list()
        self.vectorManager = None
        ids = [0, 1, 2, 3, 4]
        dates = ["1/26/20", "1/26/20", "1/26/20", "1/26/20", "1/26/20"]
        teams = ["Blue Team", "White Team", "Red Team", "Red Team", "Blue Team"]
        descriptions = ["Blue Team Defender Turns on Computer.", "White Team Analyst Starts Taking Notes.",
                        "SQL Injection attack from Red Team.", "Cross-Site Scripting Attack from Red Team.",
                        "Blue Team Defender turns off computer."]
        artifacts = ["blue_log.csv", "white_recording.png", "red_attack.txt", "red_escalation.txt", "blue_response.csv"]
        for i in range(len(descriptions)):
            logEntry = LogEntry()
            logEntry.date = dates[i]
            logEntry.description = descriptions[i]
            logEntry.creator = teams[i]
            logEntry.id = ids[i]
            logEntry.artifact = artifacts[i]
            self.logEntries[ids[i]] = logEntry
        self.logEntriesInTable = list(self.logEntries.values())

    def editLogEntryVectors(self, logEntry, logEntryRowClicked, newVectors):
        oldVectors = logEntry.associatedVectors
        logEntry.associatedVectors = newVectors
        self.vectorManager.handleUpdateToLogEntry(oldVectors, newVectors, logEntry)
        if self.searchLogEntryTableWidget != None:
            self.updateSearchLogTableEntry(logEntry, logEntryRowClicked)

    def updateSearchLogTableEntry(self, logEntry, logEntryRowClicked):
        logEntryDescriptionItem = QtWidgets.QTableWidgetItem(logEntry.description)
        if (self.logEntriesInTable[logEntryRowClicked].id == logEntry.id):
            self.searchLogEntryTableWidget.setItem(logEntryRowClicked, len(self.colNamesInSearchLogsTable) - 1,
                                               logEntryDescriptionItem)
        else:
            for i in range(len(self.logEntriesInTable)):
                if (self.logEntriesInTable[i].id == logEntry.id):
                    self.searchLogEntryTableWidget.setItem(i, len(self.colNamesInSearchLogsTable) - 1,
                                                       logEntryDescriptionItem)
                break



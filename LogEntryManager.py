import pickle

from LogEntry import LogEntry
from pathlib import Path

class LogEntryManager:
    def __init__(self):
        self.logEntries = dict()
        self.logEntriesInTable = list()
        self.filename = "logEntries.pkl"
        self.nextAvailableId = 5
        ids = [0, 1, 2, 3, 4]
        dates = ["1/31/2020 12:08 AM", "2/1/2020 11:43 PM", "2/2/2020 11:24 PM", "2/3/2020 11:01 AM", "2/4/2020 12:33 PM"]
        teams = [LogEntry.BLUE_TEAM, LogEntry.WHITE_TEAM, LogEntry.RED_TEAM, LogEntry.RED_TEAM, LogEntry.BLUE_TEAM]
        descriptions = ["Blue Team Defender Turns on Computer.", "White Team Analyst Starts Taking Notes.",
                        "SQL Injection attack from Red Team.", "Cross-Site Scripting Attack from Red Team.",
                        "Blue Team Defender turns off computer."]
        artifacts = ["blue_log.csv", "white_recording.png", "red_attack.txt", "red_escalation.txt", "blue_response.csv"]
        locations = ["Boulder, CO", "White Sands Missile Range", "UTEP Prospect Hall", "El Paso east side office",
                     "Las Cruces, NM"]
        for i in range(len(descriptions)):
            logEntry = LogEntry()
            logEntry.date = dates[i]
            logEntry.description = descriptions[i]
            logEntry.creator = teams[i]
            logEntry.eventType = teams[i]
            logEntry.id = ids[i]
            logEntry.artifact = artifacts[i]
            logEntry.locations = locations[i]
            self.logEntries[ids[i]] = logEntry
        self.logEntriesInTable = list(self.logEntries.values())

    def updateLogEntries(self, vectors):
        for vector in vectors:
            for significantEvent in list(vector.significantEvents.values()):
                if significantEvent.logEntry.id in self.logEntries:
                    self.logEntries[significantEvent.logEntry.id].associatedVectors.append(vector.vectorName)

    def storeLogEntries(self):
        with open(self.filename, 'wb') as pkl_file:
            pickle.dump(self.logEntries, pkl_file)

    def retrieveLogEntries(self):
        filename_path = Path(self.filename)
        if filename_path.exists():
            with open(self.filename, 'rb') as pkl_file:
                self.logEntries = pickle.load(pkl_file)

    def updateLogEntry(self, logEntry):
        if logEntry.id in self.logEntries:
            self.logEntries[logEntry.id] = logEntry
            return True
        return False


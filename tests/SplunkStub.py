class SplunkStub:

    def deleteLogFiles(self, source):
        return True

    def ingestLogFiles(self, source):
        return True

    def retrieveLogEntries(self, source):
        logEntries = list()
        with open(source) as fp:
            line = fp.readline()
            while line:
                logEntries.append(line)
                line = fp.readline()
        timestamps = list()
        for logEntry in logEntries:
            timestamps.append("2020-03-03 00:15:00")
        return logEntries, timestamps

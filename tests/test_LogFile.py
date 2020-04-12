from unittest import TestCase

from LogFile import LogFile
from LogEntry import LogEntry
from tests.SplunkStub import SplunkStub


class TestLogFile(TestCase):

    # Label: LF - 4
    def test_ingest_valid_log_file(self):
        logFile = LogFile(SplunkStub())
        logFile.filename = "testData/test_textual_log_file.log"
        logFile.source = "testData/test_textual_log_file.log"
        logFile.creator = "White Team"
        logFile.eventType = "White Team"
        logFile.cleanseLogFile()
        self.assertEqual(True, logFile.cleansed)
        self.assertEqual(27, len(logFile.lines))
        logFile.validateLogFile("03/01/2020 12:00 AM", "04/01/2020 12:00 AM")
        self.assertEqual(True, logFile.validated)
        logEntries = logFile.ingestLogFile()
        self.assertEqual(True, logFile.ingested)
        for logEntry in logEntries:
            self.assertEqual("03/03/2020 12:15 AM", logEntry.date)
        self.assertEqual(27, len(logEntries))

    def test_ingest_invalid_log_file(self):
        logFile = LogFile(SplunkStub())
        logFile.filename = "testData/test_textual_log_file.log"
        logFile.source = "testData/test_textual_log_file.log"
        logFile.creator = "White Team"
        logFile.eventType = "White Team"
        logFile.cleanseLogFile()
        self.assertEqual(True, logFile.cleansed)
        self.assertEqual(27, len(logFile.lines))
        logFile.validateLogFile("03/04/2020 12:00 AM", "04/01/2020 12:00 AM")
        self.assertEqual(False, logFile.validated)
        logFile.ingestLogFile()
        self.assertEqual(False, logFile.ingested)



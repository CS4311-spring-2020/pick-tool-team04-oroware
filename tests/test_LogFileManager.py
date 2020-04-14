import unittest

from LogFile import LogFile
from LogFileManager import LogFileManager
from tests.SplunkStub import SplunkStub


class TestLogFileManager(unittest.TestCase):
    def test_create_log_file(self):
        logFileManager = LogFileManager(splunkInterface=SplunkStub())
        logFileManager.col = logFileManager.db["test_files"]
        logFileManager.deleteLogFilesDb()
        self.assertEqual(True, logFileManager.createLogFile("C:/Users/marka/Desktop/software/pick-tool-team04-oroware/tests/testData/test_textual_log_file.log", "White Team", "White Team"))
        self.assertEqual(True, "C:/Users/marka/Desktop/software/pick-tool-team04-oroware/tests/testData/test_textual_log_file.log" in list(logFileManager.files.keys()))
        self.assertIsInstance(logFileManager.files["C:/Users/marka/Desktop/software/pick-tool-team04-oroware/tests/testData/test_textual_log_file.log"], LogFile)
        self.assertEqual(1, len(logFileManager.files.keys()))
        logFileManager.deleteLogFilesDb()
import unittest

from ImageLogFile import ImageLogFile


class TestAudioFile(unittest.TestCase):
    # Label: LF - 6
    def test_ingest_valid_image_file(self):
        logFile = ImageLogFile()
        logFile.filename = "testData/test_image_log_file.PNG"
        logFile.source = "testData/test_image_log_file.PNG"
        logFile.creator = "White Team"
        logFile.eventType = "White Team"
        logFile.cleanseLogFile()
        self.assertEqual(True, logFile.cleansed)
        self.assertEqual(1, len(logFile.lines))
        logFile.validateLogFile("04/10/2010 12:00 AM", "04/11/2020 1:38 PM")
        self.assertEqual(True, logFile.validated)
        logEntries = logFile.ingestLogFile()
        self.assertEqual(True, logFile.ingested)
        self.assertEqual(1, len(logEntries))
        self.assertEqual("Blue Team Defender turns off computer.", logEntries[0].description)
        self.assertEqual("4/11/2020 1:38 PM", logEntries[0].date)

    def test_ingest_invalid_image_file(self):
        logFile = ImageLogFile()
        logFile.filename = "testData/test_image_log_file.PNG"
        logFile.source = "testData/test_image_log_file.PNG"
        logFile.creator = "White Team"
        logFile.eventType = "White Team"
        logFile.cleanseLogFile()
        self.assertEqual(True, logFile.cleansed)
        self.assertEqual(1, len(logFile.lines))
        logFile.validateLogFile("4/11/2020 1:27 PM", "4/11/2020 1:37 PM")
        self.assertEqual(False, logFile.validated)
        logFile.ingestLogFile()
        self.assertEqual(False, logFile.ingested)



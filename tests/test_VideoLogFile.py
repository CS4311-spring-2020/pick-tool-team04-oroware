import unittest

from VideoLogFile import VideoLogFile


class TestAudioFile(unittest.TestCase):
    # Label: LF - 8
    def test_ingest_valid_video_file(self):
        logFile = VideoLogFile()
        logFile.filename = "testData/test_video_log_file.mp4"
        logFile.source = "testData/test_video_log_file.mp4"
        logFile.creator = "White Team"
        logFile.eventType = "White Team"
        logFile.cleanseLogFile()
        self.assertEqual(True, logFile.cleansed)
        self.assertEqual(1, len(logFile.lines))
        logFile.validateLogFile("04/10/2020 12:00 AM", "04/12/2020 12:00 AM")
        self.assertEqual(True, logFile.validated)
        logEntries = logFile.ingestLogFile()
        self.assertEqual(True, logFile.ingested)
        self.assertEqual(1, len(logEntries))
        self.assertEqual("cross-site scripting attack from red team", logEntries[0].description)
        self.assertEqual("4/11/2020 1:26 PM", logEntries[0].date)

    def test_ingest_invalid_video_file(self):
        logFile = VideoLogFile()
        logFile.filename = "testData/test_video_log_file.mp4"
        logFile.source = "testData/test_video_log_file.mp4"
        logFile.creator = "White Team"
        logFile.eventType = "White Team"
        logFile.cleanseLogFile()
        self.assertEqual(True, logFile.cleansed)
        self.assertEqual(1, len(logFile.lines))
        logFile.validateLogFile("4/11/2020 1:27 PM", "4/11/2020 1:28 PM")
        self.assertEqual(False, logFile.validated)
        logFile.ingestLogFile()
        self.assertEqual(False, logFile.ingested)



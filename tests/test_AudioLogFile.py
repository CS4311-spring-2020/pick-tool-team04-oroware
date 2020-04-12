import unittest

from AudioLogFile import AudioLogFile


class TestAudioFile(unittest.TestCase):
    # Label: LF - 5
    def test_ingest_valid_audio_file(self):
        logFile = AudioLogFile()
        logFile.filename = "testData/test_audio_log_file.wav"
        logFile.source = "testData/test_audio_log_file.wav"
        logFile.creator = "White Team"
        logFile.eventType = "White Team"
        logFile.cleanseLogFile()
        self.assertEqual(True, logFile.cleansed)
        self.assertEqual(1, len(logFile.lines))
        logFile.validateLogFile("03/01/2019 12:00 AM", "03/01/2021 12:00 AM")
        self.assertEqual(True, logFile.validated)
        logEntries = logFile.ingestLogFile()
        self.assertEqual(True, logFile.ingested)
        self.assertEqual(1, len(logEntries))
        self.assertEqual("white team analyst starts taking notes", logEntries[0].description)
        self.assertEqual("4/11/2020 9:34 AM", logEntries[0].date)

    def test_ingest_invalid_audio_file(self):
        logFile = AudioLogFile()
        logFile.filename = "testData/test_audio_log_file.wav"
        logFile.source = "testData/test_audio_log_file.wav"
        logFile.creator = "White Team"
        logFile.eventType = "White Team"
        logFile.cleanseLogFile()
        self.assertEqual(True, logFile.cleansed)
        self.assertEqual(1, len(logFile.lines))
        logFile.validateLogFile("04/04/2020 12:00 AM", "04/11/2020 12:00 AM")
        self.assertEqual(False, logFile.validated)
        logFile.ingestLogFile()
        self.assertEqual(False, logFile.ingested)



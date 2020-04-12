import unittest

from PDFLogFile import PDFLogFile


class TestPDFFile(unittest.TestCase):
    # Label: LF - 7
    def test_ingest_valid_pdf_file(self):
        logFile = PDFLogFile()
        logFile.filename = "testData/test_pdf_log_file.pdf"
        logFile.source = "testData/test_pdf_log_file.pdf"
        logFile.creator = "White Team"
        logFile.eventType = "White Team"
        logFile.cleanseLogFile()
        self.assertEqual(True, logFile.cleansed)
        self.assertEqual(1, len(logFile.lines))
        logFile.validateLogFile("01/01/2020 12:00 AM", "12/31/2020 12:00 AM")
        self.assertEqual(True, logFile.validated)
        logEntries = logFile.ingestLogFile()
        self.assertEqual(True, logFile.ingested)
        self.assertEqual(1, len(logEntries))
        self.assertEqual("Blue Team Defender turns on computer and goes to the bathroom.", logEntries[0].description)
        self.assertEqual("4/11/2020 2:09 PM", logEntries[0].date)

    def test_ingest_invalid_pdf_file(self):
        logFile = PDFLogFile()
        logFile.filename = "testData/test_pdf_log_file.pdf"
        logFile.source = "testData/test_pdf_log_file.pdf"
        logFile.creator = "White Team"
        logFile.eventType = "White Team"
        logFile.cleanseLogFile()
        self.assertEqual(True, logFile.cleansed)
        self.assertEqual(1, len(logFile.lines))
        logFile.validateLogFile("4/11/2020 2:10 PM", "4/11/2020 3:28 PM")
        self.assertEqual(False, logFile.validated)
        logFile.ingestLogFile()
        self.assertEqual(False, logFile.ingested)



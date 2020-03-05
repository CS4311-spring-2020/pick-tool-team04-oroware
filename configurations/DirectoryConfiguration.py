from PyQt5 import QtWidgets
from PyQt5.QtCore import QRunnable, pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QFileDialog, QWidget

import os


class DirectoryConfiguration(QWidget):
    def __init__(self, clientHandler):
        super(DirectoryConfiguration, self).__init__()
        self.clientHandler = clientHandler
        self.directoryTab = QtWidgets.QWidget()
        self.directoryTabLayout = QtWidgets.QVBoxLayout(self)
        self.directoryLabel = QtWidgets.QLabel(self)
        self.directoryTabLayout.addWidget(self.directoryLabel)

        self.setRootPathButton = QtWidgets.QPushButton(self)
        self.setRootPathButton.clicked.connect(self.handleSetRootPath)

        self.directoryTabLayout.addWidget(self.setRootPathButton)
        self.ingestionButton = QtWidgets.QPushButton(self)
        self.ingestionButton.clicked.connect(self.ingestLogsClicked)
        self.directoryTabLayout.addWidget(self.ingestionButton)
        self.initializeText()

    def initializeText(self):
        self.directoryLabel.setText("Current Root Path: " + str(self.clientHandler.logFileManager.rootPath))
        self.ingestionButton.setText("Start Data Ingestion")
        self.setRootPathButton.setText('Change Root Path')

    def ingestLogs(self, root):
        if self.clientHandler.eventConfig.eventStartTime != None and self.clientHandler.eventConfig.eventEndTime != None and root != None:
            redTeamPath = root + "/red/"
            blueTeamPath = root + "/blue/"
            whiteTeamPath = root + "/white/"

            for filename in os.listdir(redTeamPath):
                self.clientHandler.logFileManager.createLogFile(redTeamPath + filename, "Red Team", "Red Team")
            for filename in os.listdir(blueTeamPath):
                self.clientHandler.logFileManager.createLogFile(blueTeamPath + filename, "Blue Team", "Blue Team")

            for filename in os.listdir(whiteTeamPath):
                self.clientHandler.logFileManager.createLogFile(whiteTeamPath + filename, "White Team", "White Team")

            self.clientHandler.logFileManager.storeLogFiles()

            self.threadpool = QThreadPool()
            ingestionWorker = IngestionWorker(self.clientHandler)
            self.threadpool.start(ingestionWorker)

    def handleSetRootPath(self):
        self.fileDialog = QFileDialog()
        self.clientHandler.logFileManager.rootPath = self.fileDialog.getExistingDirectory()
        self.clientHandler.logFileManager.storeLogFiles()
        self.initializeText()

    def ingestLogsClicked(self):
        if self.clientHandler.logFileManager.rootPath != None:
            self.ingestLogs(self.clientHandler.logFileManager.rootPath)


class IngestionWorker(QRunnable):

    def __init__(self, clientHandler):
        super(IngestionWorker, self).__init__()
        self.clientHandler = clientHandler

    @pyqtSlot()
    def run(self):
        eventStartTime = self.clientHandler.eventConfig.eventStartTime
        eventEndTime = self.clientHandler.eventConfig.eventEndTime
        logFiles = list(self.clientHandler.logFileManager.files.values())
        for logFile in logFiles:
            logEntries = self.ingestLogFile(logFile, eventStartTime, eventEndTime)
            if logEntries != None:
                self.clientHandler.sendLogEntries(logEntries)
                self.clientHandler.logFileManager.storeLogFiles()

    def ingestLogFile(self, logFile, eventStartTime, eventEndTime):
        logEntries = list()
        if logFile.cleanseLogFile():
            if logFile.validateLogFile(eventStartTime, eventEndTime):
                logEntries = logFile.ingestLogFile()
        return logEntries
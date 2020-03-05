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


        # Intialize Directory Configuration
        # self.rootConfiguration = QtWidgets.QFrame(self)
        # self.rootConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        # self.rootConfigurationLayout = QtWidgets.QVBoxLayout(self.rootConfiguration)
        # self.directoryConfigurationLabel = QtWidgets.QLabel(self.rootConfiguration)
        # self.rootConfigurationLayout.addWidget(self.directoryConfigurationLabel)
        # self.rootLabel = QtWidgets.QLabel(self.rootConfiguration)
        # self.rootConfigurationLayout.addWidget(self.rootLabel)
        # self.rootDialog = QFileDialog()
        # self.rootDialog.setFileMode(QFileDialog.DirectoryOnly)
        # self.rootConfigurationLayout.addWidget(self.rootDialog)
        # self.directoryTabLayout.addWidget(self.rootConfiguration)

        # self.redTeamConfiguration = QtWidgets.QFrame(self)
        # self.redTeamConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        # self.redTeamConfigurationLayout = QtWidgets.QVBoxLayout(self.redTeamConfiguration)
        # self.redTeamLabel = QtWidgets.QLabel(self.redTeamConfiguration)
        # self.redTeamConfigurationLayout.addWidget(self.redTeamLabel)
        # self.redTeamDialog = QFileDialog()
        # self.redTeamDialog.setFileMode(QFileDialog.DirectoryOnly)
        # self.redTeamConfigurationLayout.addWidget(self.redTeamDialog)
        # self.directoryTabLayout.addWidget(self.redTeamConfiguration)

        # self.blueTeamConfiguration = QtWidgets.QFrame(self)
        # self.blueTeamConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        # self.blueTeamConfigurationLayout = QtWidgets.QVBoxLayout(self.blueTeamConfiguration)
        # self.blueTeamLabel = QtWidgets.QLabel(self.blueTeamConfiguration)
        # self.blueTeamConfigurationLayout.addWidget(self.blueTeamLabel)
        # self.blueTeamDialog = QFileDialog()
        # self.blueTeamDialog.setFileMode(QFileDialog.DirectoryOnly)
        # self.blueTeamConfigurationLayout.addWidget(self.blueTeamDialog)
        # self.directoryTabLayout.addWidget(self.blueTeamConfiguration)

        # self.whiteTeamConfiguration = QtWidgets.QFrame(self)
        # self.whiteTeamConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        # self.whiteTeamConfigurationLayout = QtWidgets.QVBoxLayout(self.whiteTeamConfiguration)
        # self.whiteTeamLabel = QtWidgets.QLabel(self.whiteTeamConfiguration)
        # self.whiteTeamConfigurationLayout.addWidget(self.whiteTeamLabel)
        # self.whiteTeamDialog = QFileDialog()
        # self.whiteTeamDialog.setFileMode(QFileDialog.DirectoryOnly)
        # self.whiteTeamConfigurationLayout.addWidget(self.whiteTeamDialog)
        # self.ingestionButton = QtWidgets.QPushButton(self.whiteTeamConfiguration)
        # self.whiteTeamConfigurationLayout.addWidget(self.ingestionButton)
        # self.directoryTabLayout.addWidget(self.whiteTeamConfiguration)
        # self.initializeText()

    def initializeText(self):
        # self.whiteTeamLabel.setText("White Team Folder: ")
        # self.rootLabel.setText("Root Directory: ")
        # self.blueTeamLabel.setText("Blue Team Folder: ")
        self.directoryLabel.setText("DIRECTORY CONFIGURATION")
        # self.redTeamLabel.setText("Red Team Folder: ")
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
        # self.setPathPopup = SetRootPathPopup(self.clientHandler)
        # self.setPathPopup.setGeometry(100, 200, 700, 500)
        # self.setPathPopup.show()
        self.fileDialog = QFileDialog()
        self.clientHandler.logFileManager.rootPath = self.fileDialog.getExistingDirectory()

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
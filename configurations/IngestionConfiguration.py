from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QRunnable, pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QFileDialog

import os


class IngestionConfiguration(QWidget):
    def __init__(self, clientHandler):
        super(IngestionConfiguration, self).__init__()
        self.clientHandler = clientHandler
        self.ingestionTabLayout = QtWidgets.QVBoxLayout(self)

        # Initialize Directory Configuration
        self.directoryConfigurationFrame = QtWidgets.QFrame(self)
        self.directoryConfigurationFrame.setFrameShape(QtWidgets.QFrame.Box)

        self.directoryConfigurationLayout = QtWidgets.QVBoxLayout(self.directoryConfigurationFrame)
        self.directoryConfigurationLabel = QtWidgets.QLabel(self.directoryConfigurationFrame)
        self.directoryConfigurationLayout.addWidget(self.directoryConfigurationLabel)

        self.rootPathLabel = QtWidgets.QLabel(self.directoryConfigurationFrame)
        self.directoryConfigurationLayout.addWidget(self.rootPathLabel)
        self.rootPathField = QtWidgets.QLineEdit(self.directoryConfigurationFrame)
        self.rootPathField.setEnabled(False)
        self.directoryConfigurationLayout.addWidget(self.rootPathField)
        self.setRootPathButton = QtWidgets.QPushButton(self)
        self.setRootPathButton.clicked.connect(self.handleSetRootPath)

        self.directoryConfigurationLayout.addWidget(self.setRootPathButton)
        self.ingestionButton = QtWidgets.QPushButton(self)
        self.ingestionButton.clicked.connect(self.ingestLogsClicked)
        self.directoryConfigurationLayout.addWidget(self.ingestionButton)
        self.ingestionTabLayout.addWidget(self.directoryConfigurationFrame)

        # Initialize Log File Configuration
        # --------------------------------------------------------------------------------------------------------------
        # Log File Table
        self.colsLogFileTable = ["Filename", "Source", "Cleansing Status", "Validation Status", "Ingestion Status",
                                 "View Enforcement Action Report"]
        self.colsEnfActRepTable = ["Filename", "Line Number", "Error Message", "Validate", "Cancel"]

        self.logFileConfigurationFrame = QtWidgets.QFrame(self)
        self.logFileConfigurationFrame.setFrameShape(QtWidgets.QFrame.Box)

        self.logFileConfigurationLayout = QtWidgets.QVBoxLayout(self.logFileConfigurationFrame)
        self.logFileConfigurationLabel = QtWidgets.QLabel(self.logFileConfigurationFrame)
        self.logFileConfigurationLayout.addWidget(self.logFileConfigurationLabel)

        self.logFileTableContainer = QtWidgets.QWidget(self)
        self.logFileTableContainerLayout = QtWidgets.QVBoxLayout(self.logFileTableContainer)

        self.logFileTableLabel = QtWidgets.QLabel(self.logFileTableContainer)
        self.logFileTableContainerLayout.addWidget(self.logFileTableLabel)

        self.logFileTableWidget = QtWidgets.QTableWidget(self.logFileTableContainer)
        self.logFileTableWidget.setColumnCount(0)
        self.logFileTableWidget.setRowCount(0)
        self.logFileTableContainerLayout.addWidget(self.logFileTableWidget)

        self.logFileConfigurationLayout.addWidget(self.logFileTableContainer)
        # --------------------------------------------------------------------------------------------------------------
        # Enforcement Action Report Table
        self.enfActRepTableContainer = QtWidgets.QWidget(self)
        self.enfActRepTableContainerLayout = QtWidgets.QVBoxLayout(self.enfActRepTableContainer)

        self.enfActRepTableLabel = QtWidgets.QLabel(self.enfActRepTableContainer)
        self.enfActRepTableContainerLayout.addWidget(self.enfActRepTableLabel)

        self.enfActRepTableWidget = QtWidgets.QTableWidget(self.enfActRepTableContainer)
        self.enfActRepTableWidget.setColumnCount(0)
        self.enfActRepTableWidget.setRowCount(0)
        self.enfActRepTableContainerLayout.addWidget(self.enfActRepTableWidget)

        self.logFileConfigurationLayout.addWidget(self.enfActRepTableContainer)
        self.ingestionTabLayout.addWidget(self.logFileConfigurationFrame)
        # --------------------------------------------------------------------------------------------------------------
        self.initializeText()
        self.updateLogFileTable()
        self.updateEnfActRepTable()

    def onTabChange(self):
        self.logFileTableWidget.clear()
        self.enfActRepTableWidget.clear()
        self.updateLogFileTable()
        self.updateEnfActRepTable()

    def initializeText(self):
        self.enfActRepTableLabel.setText("Enforcement Action Report Table")
        self.enfActRepTableLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.logFileTableLabel.setText("Log File Table")
        self.logFileTableLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.logFileConfigurationLabel.setText("LOG FILE CONFIGURATION")
        self.logFileConfigurationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.directoryConfigurationLabel.setText("DIRECTORY CONFIGURATION")
        self.directoryConfigurationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.ingestionButton.setText("Start Data Ingestion")
        self.ingestionButton.setFont(QtGui.QFont('SansSerif', 7))
        self.setRootPathButton.setText("Change Root Path")
        self.setRootPathButton.setFont(QtGui.QFont('SansSerif', 7))
        self.rootPathField.setText(self.clientHandler.logFileManager.rootPath)
        self.rootPathField.setFont(QtGui.QFont('SansSerif', 7))
        self.rootPathLabel.setText("Current Root Directory:")
        self.rootPathLabel.setFont(QtGui.QFont('SansSerif', 7))

    def handleSetRootPath(self):
        self.fileDialog = QFileDialog()
        self.clientHandler.logFileManager.rootPath = self.fileDialog.getExistingDirectory()
        self.rootPathField.setText(self.clientHandler.logFileManager.rootPath)
        self.clientHandler.logFileManager.storeRootPath()
        self.initializeText()

    def ingestLogsClicked(self):
        if self.clientHandler.logFileManager.rootPath != None:
            self.ingestLogs(self.clientHandler.logFileManager.rootPath)
        else:
            print("No root path selected.")
            return

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

            self.updateLogFileTable()
            self.updateEnfActRepTable()
            self.clientHandler.logFileManager.storeLogFiles()

            self.threadpool = QThreadPool()
            ingestionWorker = IngestionWorker(self.clientHandler)
            self.threadpool.start(ingestionWorker)

    def updateLogFileTable(self):
        logFiles = self.clientHandler.logFileManager.files
        totalRows = len(logFiles)

        self.logFileTableWidget.setColumnCount(len(self.colsLogFileTable))
        self.logFileTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logFileTableWidget.setRowCount(totalRows)

        header = self.logFileTableWidget.horizontalHeader()

        for col in range(len(self.colsLogFileTable)):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsLogFileTable[col])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.logFileTableWidget.setHorizontalHeaderItem(col, headerItem)

        counter = 0
        for filename, logFile in logFiles.items():
            logFileFilenameItem = QtWidgets.QTableWidgetItem(filename)
            logFileFilenameItem.setFont(QtGui.QFont('SansSerif', 7))
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("Filename"), logFileFilenameItem)

            logFileSourceItem = QtWidgets.QTableWidgetItem(logFile.source)
            logFileSourceItem.setFont(QtGui.QFont('SansSerif', 7))
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("Source"), logFileSourceItem)

            logFileCleansingStatus = ("Cleansed" if logFile.cleansed else "Uncleansed")
            logFileCleansingStatusItem = QtWidgets.QTableWidgetItem(logFileCleansingStatus)
            logFileCleansingStatusItem.setFont(QtGui.QFont('SansSerif', 7))
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("Cleansing Status"),
                                            logFileCleansingStatusItem)

            logFileValidationStatusItem = QtWidgets.QTableWidgetItem("Validated" if logFile.validated else "Not Validated")
            logFileValidationStatusItem.setFont(QtGui.QFont('SansSerif', 7))
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("Validation Status"),
                                            logFileValidationStatusItem)

            logFileIngestionStatus = ("Ingested" if logFile.ingested else "Not Ingested")
            logFileIngestionStatusItem = QtWidgets.QTableWidgetItem(logFileIngestionStatus)
            logFileIngestionStatusItem.setFont(QtGui.QFont('SansSerif', 7))
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("Ingestion Status"),
                                            logFileIngestionStatusItem)

            logFileViewReportItem = QtWidgets.QTableWidgetItem("<button goes here>")
            logFileViewReportItem.setFont(QtGui.QFont('SansSerif', 7))
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("View Enforcement Action Report"),
                                            logFileViewReportItem)

            counter += 1

    def updateEnfActRepTable(self):
        reportFiles = self.clientHandler.logFileManager.files
        totalRows = len(reportFiles)

        self.enfActRepTableWidget.setColumnCount(len(self.colsEnfActRepTable))
        self.enfActRepTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.enfActRepTableWidget.setRowCount(totalRows)

        header = self.enfActRepTableWidget.horizontalHeader()

        for col in range(len(self.colsEnfActRepTable)):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsEnfActRepTable[col])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.enfActRepTableWidget.setHorizontalHeaderItem(col, headerItem)

        counter = 0
        for filename, reportFile in reportFiles.items():
            reportFileFilenameItem = QtWidgets.QTableWidgetItem(filename)
            reportFileFilenameItem.setFont(QtGui.QFont('SansSerif', 7))
            self.enfActRepTableWidget.setItem(counter, self.colsEnfActRepTable.index("Filename"),
                                              reportFileFilenameItem)

            reportFileLineNumberItem = QtWidgets.QTableWidgetItem(str(reportFile.invalidLineNumber))
            reportFileLineNumberItem.setFont(QtGui.QFont('SansSerif', 7))
            self.enfActRepTableWidget.setItem(counter, self.colsEnfActRepTable.index("Line Number"),
                                              reportFileLineNumberItem)

            reportFileErrMsgItem = QtWidgets.QTableWidgetItem(reportFile.errorMessage)
            reportFileErrMsgItem.setFont(QtGui.QFont('SansSerif', 7))
            self.enfActRepTableWidget.setItem(counter, self.colsEnfActRepTable.index("Error Message"),
                                              reportFileErrMsgItem)

            reportFileValidateItem = QtWidgets.QTableWidgetItem("<Validate Button goes here>")
            reportFileValidateItem.setFont(QtGui.QFont('SansSerif', 7))
            self.enfActRepTableWidget.setItem(counter, self.colsEnfActRepTable.index("Validate"),
                                              reportFileValidateItem)

            reportFileCancelItem = QtWidgets.QTableWidgetItem("<Cancel Button goes here>")
            reportFileCancelItem.setFont(QtGui.QFont('SansSerif', 7))
            self.enfActRepTableWidget.setItem(counter, self.colsEnfActRepTable.index("Cancel"),
                                              reportFileCancelItem)

            counter += 1


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
                self.clientHandler.logFileManager.storeLogFileDb(logFile)

    def ingestLogFile(self, logFile, eventStartTime, eventEndTime):
        logEntries = list()
        if logFile.cleanseLogFile():
            if logFile.validateLogFile(eventStartTime, eventEndTime):
                logEntries = logFile.ingestLogFile()
        return logEntries
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QTableWidgetItem


class LogFileConfiguration(QWidget):
    def __init__(self, clientHandler):
        super(LogFileConfiguration, self).__init__()
        self.clientHandler = clientHandler
        # --------------------------------------------------------------------------------------------------------------
        # Log File Table
        self.colsLogFileTable = ["Filename", "Source", "Cleansing Status", "Validation Status", "Ingestion Status",
                                 "View Enforcement Action Report"]
        self.colsEnfActRepTable = ["Filename", "Line Number", "Error Message", "Validate", "Cancel"]

        self.logFileConfigurationLayout = QtWidgets.QVBoxLayout(self)

        self.logFileTableContainer = QtWidgets.QWidget(self)
        self.logFileTableContainerLayout = QtWidgets.QVBoxLayout(self.logFileTableContainer)

        self.logFileTableLabel = QtWidgets.QLabel(self.logFileTableContainer)
        self.logFileTableContainerLayout.addWidget(self.logFileTableLabel)

        self.logFileTableWidget = QtWidgets.QTableWidget(self.logFileTableContainer)
        self.logFileTableWidget.setColumnCount(0)
        self.logFileTableWidget.setRowCount(0)
        self.logFileTableWidget.setMinimumSize(1250, 1750)
        self.logFileTableContainerLayout.addWidget(self.logFileTableWidget)

        self.logFileConfigurationLayout.addWidget(self.logFileTableContainer)
        # --------------------------------------------------------------------------------------------------------------
        # Enforcement Action Report Table
        self.enfActRepTableContainer = QtWidgets.QWidget(self)
        self.enfActRepTableContainerLayout = QtWidgets.QVBoxLayout(self.enfActRepTableContainer)

        self.enfActRepTableLabel = QtWidgets.QLabel(self.enfActRepTableContainer)
        self.enfActRepTableContainerLayout.addWidget(self.enfActRepTableLabel)

        self.enfActRepTableWidget = QtWidgets.QTableWidget(self)
        self.enfActRepTableWidget.setColumnCount(0)
        self.enfActRepTableWidget.setRowCount(0)
        self.enfActRepTableWidget.setMinimumSize(1250, 1750)
        self.enfActRepTableContainerLayout.addWidget(self.enfActRepTableWidget)

        self.logFileConfigurationLayout.addWidget(self.enfActRepTableContainer)
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
        self.logFileTableLabel.setText("Log File Table")

    def updateLogFileTable(self):
        logFiles = self.clientHandler.logFileManager.files
        totalRows = len(logFiles)

        self.logFileTableWidget.setColumnCount(len(self.colsLogFileTable))
        self.logFileTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logFileTableWidget.setRowCount(totalRows)

        header = self.logFileTableWidget.horizontalHeader()

        for col in range(len(self.colsLogFileTable)):
            self.logFileTableWidget.setColumnWidth(col, 200)
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            self.logFileTableWidget.setHorizontalHeaderItem(col, QTableWidgetItem(self.colsLogFileTable[col]))

        counter = 0;
        for filename, logFile in logFiles.items():
            logFileFilenameItem = QtWidgets.QTableWidgetItem(filename)
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("Filename"), logFileFilenameItem)

            logFileSourceItem = QtWidgets.QTableWidgetItem(logFile.source)
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("Source"), logFileSourceItem)

            logFileCleansingStatus = ("Cleansed" if logFile.cleansed else "Uncleansed")
            logFileCleansingStatusItem = QtWidgets.QTableWidgetItem(logFileCleansingStatus)
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("Cleansing Status"),
                                            logFileCleansingStatusItem)

            logFileValidationStatusItem = QtWidgets.QTableWidgetItem(logFile.validated)
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("Validation Status"),
                                            logFileValidationStatusItem)

            logFileIngestionStatus = ("Ingested" if logFile.ingested else "Not Ingested")
            logFileIngestionStatusItem = QtWidgets.QTableWidgetItem(logFileIngestionStatus)
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("Ingestion Status"),
                                            logFileIngestionStatusItem)

            logFileViewReportItem = QtWidgets.QTableWidgetItem("<button goes here>")
            self.logFileTableWidget.setItem(counter, self.colsLogFileTable.index("View Enforcement Action Report"),
                                            logFileViewReportItem)

            counter += 1

    def updateEnfActRepTable(self):
        reportFiles = self.clientHandler.logFileManager.files
        totalRows = len(reportFiles)

        self.enfActRepTableWidget.setColumnCount(len(self.colsEnfActRepTable))
        self.enfActRepTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.enfActRepTableWidget.setRowCount(totalRows)

        header = self.logFileTableWidget.horizontalHeader()

        for col in range(len(self.colsEnfActRepTable)):
            self.enfActRepTableWidget.setColumnWidth(col, 365)
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            self.enfActRepTableWidget.setHorizontalHeaderItem(col, QTableWidgetItem(self.colsEnfActRepTable[col]))

        counter = 0
        for filename, reportFile in reportFiles.items():
            reportFileFilenameItem = QtWidgets.QTableWidgetItem(filename)
            self.enfActRepTableWidget.setItem(counter, self.colsEnfActRepTable.index("Filename"),
                                              reportFileFilenameItem)

            reportFileLineNumberItem = QtWidgets.QTableWidgetItem(str(reportFile.invalidLineNumber))
            self.enfActRepTableWidget.setItem(counter, self.colsEnfActRepTable.index("Line Number"),
                                              reportFileLineNumberItem)

            reportFileErrMsgItem = QtWidgets.QTableWidgetItem(reportFile.errorMessage)
            self.enfActRepTableWidget.setItem(counter, self.colsEnfActRepTable.index("Error Message"),
                                              reportFileErrMsgItem)

            reportFileValidateItem = QtWidgets.QTableWidgetItem("<Validate Button goes here>")
            self.enfActRepTableWidget.setItem(counter, self.colsEnfActRepTable.index("Validate"),
                                              reportFileValidateItem)

            reportFileCancelItem = QtWidgets.QTableWidgetItem("<Cancel Button goes here>")
            self.enfActRepTableWidget.setItem(counter, self.colsEnfActRepTable.index("Cancel"),
                                              reportFileCancelItem)

            counter += 1
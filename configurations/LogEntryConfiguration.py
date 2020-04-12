from datetime import datetime

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QWidget

from LogEntryPopup import LogEntryPopup


class LogEntryConfiguration(QWidget):
    def __init__(self, clientHandler):
        super(LogEntryConfiguration, self).__init__()
        self.colsSearchLogsTable = ["Timestamp", "Content", "Artifact", "Creator", "Event Type", "Location", "Vectors"]
        self.clientHandler = clientHandler
        self.searchLogsTab = QtWidgets.QWidget()
        self.searchLogsLayout = QtWidgets.QVBoxLayout(self)
        self.keywordSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.keywordSearchLabel)
        self.commandSearchTextEdit = QtWidgets.QPlainTextEdit(self)
        self.commandSearchTextEdit.setMaximumHeight(25)
        self.commandSearchTextEdit.setFont(QtGui.QFont('SansSerif', 7))
        self.searchLogsLayout.addWidget(self.commandSearchTextEdit)
        self.creatorSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.creatorSearchLabel)
        self.creatorCheckboxes = QtWidgets.QWidget(self)
        self.creatorCheckboxesLayout = QtWidgets.QHBoxLayout(self.creatorCheckboxes)
        self.creatorBlueTeamCheckBox = QtWidgets.QCheckBox(self.creatorCheckboxes)
        self.creatorCheckboxesLayout.addWidget(self.creatorBlueTeamCheckBox)
        self.creatorWhiteTeamCheckBox = QtWidgets.QCheckBox(self.creatorCheckboxes)
        self.creatorCheckboxesLayout.addWidget(self.creatorWhiteTeamCheckBox)
        self.creatorRedTeamCheckBox = QtWidgets.QCheckBox(self.creatorCheckboxes)
        self.creatorCheckboxesLayout.addWidget(self.creatorRedTeamCheckBox)
        self.searchLogsLayout.addWidget(self.creatorCheckboxes)
        self.eventTypeSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.eventTypeSearchLabel)
        self.eventCheckboxes = QtWidgets.QWidget(self)
        self.eventCheckboxesLayout = QtWidgets.QHBoxLayout(self.eventCheckboxes)
        self.eventTypeBlueTeamCheckBox = QtWidgets.QCheckBox(self.eventCheckboxes)
        self.eventCheckboxesLayout.addWidget(self.eventTypeBlueTeamCheckBox)
        self.eventTypeWhiteTeamCheckBox = QtWidgets.QCheckBox(self.eventCheckboxes)
        self.eventCheckboxesLayout.addWidget(self.eventTypeWhiteTeamCheckBox)
        self.eventTypeRedTeamCheckBox = QtWidgets.QCheckBox(self.eventCheckboxes)
        self.eventCheckboxesLayout.addWidget(self.eventTypeRedTeamCheckBox)
        self.searchLogsLayout.addWidget(self.eventCheckboxes)
        # Added Location search criteria
        self.locationSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.locationSearchLabel)
        self.locationSearchTextEdit = QtWidgets.QPlainTextEdit(self)
        self.locationSearchTextEdit.setMaximumHeight(25)
        self.searchLogsLayout.addWidget(self.locationSearchTextEdit)
        # End Location variables
        self.fromSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.fromSearchLabel)
        self.fromDateTimeEditSearchLogs = QtWidgets.QDateTimeEdit(self)
        self.fromDateTimeEditSearchLogs.setDisplayFormat("M/d/yyyy hh:mm A")
        self.fromDateTimeEditSearchLogs.setFont(QtGui.QFont('SansSerif', 7))
        self.searchLogsLayout.addWidget(self.fromDateTimeEditSearchLogs)
        self.toSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.toSearchLabel)
        self.toDateTimeEditSearchLogs = QtWidgets.QDateTimeEdit(self)
        self.toDateTimeEditSearchLogs.setDisplayFormat("M/d/yyyy hh:mm A")
        self.toDateTimeEditSearchLogs.setFont(QtGui.QFont('SansSerif', 7))
        self.searchLogsLayout.addWidget(self.toDateTimeEditSearchLogs)
        self.searchButton = QtWidgets.QPushButton(self)
        self.searchLogsLayout.addWidget(self.searchButton)
        # Connects Apply Filter button to method handleSearchButtonClicked
        self.searchButton.clicked.connect(self.handleSearchButtonClicked)
        self.searchLogsTableWidget = QtWidgets.QTableWidget(self)
        self.searchLogsTableWidget.setColumnCount(0)
        self.searchLogsTableWidget.setRowCount(0)
        self.searchLogsLayout.addWidget(self.searchLogsTableWidget)
        self.intializeText()
        self.updateLogTable()

    def intializeText(self):
        self.keywordSearchLabel.setText("Keyword Search:")
        self.keywordSearchLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.creatorSearchLabel.setText("Creator:")
        self.creatorSearchLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.creatorBlueTeamCheckBox.setText("Blue Team")
        self.creatorBlueTeamCheckBox.setFont(QtGui.QFont('SansSerif', 7))
        self.creatorWhiteTeamCheckBox.setText("White Team")
        self.creatorWhiteTeamCheckBox.setFont(QtGui.QFont('SansSerif', 7))
        self.creatorRedTeamCheckBox.setText("Red Team")
        self.creatorRedTeamCheckBox.setFont(QtGui.QFont('SansSerif', 7))
        self.eventTypeBlueTeamCheckBox.setText("Blue Team")
        self.eventTypeBlueTeamCheckBox.setFont(QtGui.QFont('SansSerif', 7))
        self.eventTypeWhiteTeamCheckBox.setText("White Team")
        self.eventTypeWhiteTeamCheckBox.setFont(QtGui.QFont('SansSerif', 7))
        self.eventTypeRedTeamCheckBox.setText("Red Team")
        self.eventTypeRedTeamCheckBox.setFont(QtGui.QFont('SansSerif', 7))
        self.eventTypeSearchLabel.setText("Event Type:")
        self.eventTypeSearchLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.locationSearchLabel.setText("Location:")
        self.locationSearchLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.fromSearchLabel.setText("Start Timestamp:")
        self.fromSearchLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.toSearchLabel.setText("End Timestamp:")
        self.toSearchLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.searchButton.setText("Apply Filter")
        self.searchButton.setFont(QtGui.QFont('SansSerif', 7))

    def searchTableDoubleClicked(self):
        logEntryLineNumber = self.searchLogsTableWidget.verticalHeaderItem(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        logEntryArtifact = self.searchLogsTableWidget.item(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Artifact")).text()
        logEntryId = logEntryArtifact + "_" + logEntryLineNumber
        logEntry = self.clientHandler.logEntryManager.logEntries[logEntryId]
        logEntryDescriptionWidget = self.searchLogsTableWidget.item(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Content"))
        logEntryLocationWidget = self.searchLogsTableWidget.item(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Location"))
        logEntryEventWidget = self.searchLogsTableWidget.item(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Event Type"))
        associatedVectorsWidget = self.searchLogsTableWidget.cellWidget(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Vectors"))
        self.editPopup = LogEntryPopup(logEntry, logEntryDescriptionWidget, logEntryLocationWidget, logEntryEventWidget, associatedVectorsWidget, self.clientHandler)
        self.editPopup.setGeometry(100, 200, 200, 200)
        self.editPopup.show()

    def handleSearchButtonClicked(self):
        commandSearch = self.commandSearchTextEdit.toPlainText()
        creatorBlueTeam = self.creatorBlueTeamCheckBox.isChecked()
        creatorWhiteTeam = self.creatorWhiteTeamCheckBox.isChecked()
        creatorRedTeam = self.creatorRedTeamCheckBox.isChecked()
        eventTypeBlueTeam = self.eventTypeBlueTeamCheckBox.isChecked()
        eventTypeWhiteTeam = self.eventTypeWhiteTeamCheckBox.isChecked()
        eventTypeRedTeam = self.eventTypeRedTeamCheckBox.isChecked()
        startTime = self.fromDateTimeEditSearchLogs.text()
        endTime = self.toDateTimeEditSearchLogs.text()
        locationSearch = self.locationSearchTextEdit.toPlainText()
        if (datetime.strptime(endTime, "%m/%d/%Y %I:%M %p") <= datetime.strptime(startTime, "%m/%d/%Y %I:%M %p")):
            print("Invalid start or end time.")
            return
        self.clientHandler.searchLogEntries(commandSearch, creatorBlueTeam, creatorWhiteTeam, creatorRedTeam, eventTypeBlueTeam, eventTypeWhiteTeam, eventTypeRedTeam, startTime, endTime, locationSearch)
        self.updateLogTable()

    def updateLogTable(self):
        logEntries = self.clientHandler.logEntryManager.logEntriesInTable
        totalRows = len(logEntries)
        self.searchLogsTableWidget.setColumnCount(len(self.colsSearchLogsTable))
        self.searchLogsTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.searchLogsTableWidget.setRowCount(totalRows)
        header = self.searchLogsTableWidget.horizontalHeader()
        for colNum in range(len(self.colsSearchLogsTable)):
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsSearchLogsTable[colNum])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.searchLogsTableWidget.setHorizontalHeaderItem(colNum, headerItem)
        for rowNum in range(totalRows):
            logEntryLineNumberItem = QtWidgets.QTableWidgetItem(str(logEntries[rowNum].lineNumber))
            logEntryLineNumberItem.setFont(QtGui.QFont('SansSerif', 7))
            self.searchLogsTableWidget.setVerticalHeaderItem(rowNum, logEntryLineNumberItem)
            self.searchLogsTableWidget.setRowHeight(rowNum, 50)
            logEntryDescriptionItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].description)
            logEntryDescriptionItem.setFont(QtGui.QFont('SansSerif', 7))
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Content"), logEntryDescriptionItem)
            logEntryTeamItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].creator)
            logEntryTeamItem.setFont(QtGui.QFont('SansSerif', 7))
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Creator"), logEntryTeamItem)
            logEntryArtifactItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].artifact)
            logEntryArtifactItem.setFont(QtGui.QFont('SansSerif', 7))
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Artifact"), logEntryArtifactItem)
            logEntryEventTypeItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].eventType)
            logEntryEventTypeItem.setFont(QtGui.QFont('SansSerif', 7))
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Event Type"), logEntryEventTypeItem)
            # Populate Location column
            logEntryLocationItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].location)
            logEntryLocationItem.setFont(QtGui.QFont('SansSerif', 7))
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Location"), logEntryLocationItem)
            # End populate Location column
            logEntryDateItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].date)
            logEntryDateItem.setFont(QtGui.QFont('SansSerif', 7))
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Timestamp"), logEntryDateItem)
            logEntries[rowNum].rowIndexInTable = rowNum
            vectorComboBoxSearchTable = CheckableComboBox(logEntries[rowNum], self.clientHandler)
            counter = 0
            for vector in self.clientHandler.vectorManager.vectors.values():
                vectorComboBoxSearchTable.addItem(vector.vectorName)
                item = vectorComboBoxSearchTable.model().item(counter, 0)
                if vector.vectorName in logEntries[rowNum].associatedVectors:
                    item.setCheckState(QtCore.Qt.Checked)
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)
                counter += 1
            self.searchLogsTableWidget.setCellWidget(rowNum, self.colsSearchLogsTable.index("Vectors"), vectorComboBoxSearchTable)
        self.searchLogsTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.searchLogsTableWidget.doubleClicked.connect(self.searchTableDoubleClicked)

class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self, logEntry, clientHandler):
        super(CheckableComboBox, self).__init__()
        self.setFont(QtGui.QFont('SansSerif', 7))
        self.logEntry = logEntry
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))
        self.clientHandler = clientHandler

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)
        newVectors = list()
        for i in range(self.count()):
            if self.model().item(i, 0).checkState() == QtCore.Qt.Checked:
                newVectors.append(self.model().itemFromIndex(index).text())
        self.clientHandler.editLogEntryVectors(self.logEntry, newVectors)
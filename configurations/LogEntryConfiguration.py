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
        self.filterConfigurationLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.filterConfigurationLabel)
        self.keywordSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.keywordSearchLabel)
        self.commandSearchTextEdit = QtWidgets.QPlainTextEdit(self)
        self.searchLogsLayout.addWidget(self.commandSearchTextEdit)
        self.creatorSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.creatorSearchLabel)
        self.creatorBlueTeamCheckBox = QtWidgets.QCheckBox(self)
        self.searchLogsLayout.addWidget(self.creatorBlueTeamCheckBox)
        self.creatorWhiteTeamCheckBox = QtWidgets.QCheckBox(self)
        self.searchLogsLayout.addWidget(self.creatorWhiteTeamCheckBox)
        self.creatorRedTeamCheckBox = QtWidgets.QCheckBox(self)
        self.searchLogsLayout.addWidget(self.creatorRedTeamCheckBox)
        self.eventTypeSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.eventTypeSearchLabel)
        self.eventTypeBlueTeamCheckBox = QtWidgets.QCheckBox(self)
        self.searchLogsLayout.addWidget(self.eventTypeBlueTeamCheckBox)
        self.eventTypeWhiteTeamCheckBox = QtWidgets.QCheckBox(self)
        self.searchLogsLayout.addWidget(self.eventTypeWhiteTeamCheckBox)
        self.eventTypeRedTeamCheckBox = QtWidgets.QCheckBox(self)
        self.searchLogsLayout.addWidget(self.eventTypeRedTeamCheckBox)
        # Added Location search criteria
        self.locationSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.locationSearchLabel)
        self.locationSearchTextEdit = QtWidgets.QPlainTextEdit(self)
        self.searchLogsLayout.addWidget(self.locationSearchTextEdit)
        # End Location variables
        self.fromSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.fromSearchLabel)
        self.fromDateTimeEditSearchLogs = QtWidgets.QDateTimeEdit(self)
        self.searchLogsLayout.addWidget(self.fromDateTimeEditSearchLogs)
        self.toSearchLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.toSearchLabel)
        self.toDateTimeEditSearchLogs = QtWidgets.QDateTimeEdit(self)
        self.searchLogsLayout.addWidget(self.toDateTimeEditSearchLogs)
        self.searchButton = QtWidgets.QPushButton(self)
        self.searchLogsLayout.addWidget(self.searchButton)
        # Connects Apply Filter button to method handleSearchButtonClicked
        self.searchButton.clicked.connect(self.handleSearchButtonClicked)
        self.logEntryConfigurationLabel = QtWidgets.QLabel(self)
        self.searchLogsLayout.addWidget(self.logEntryConfigurationLabel)
        self.searchLogsTableWidget = QtWidgets.QTableWidget(self)
        self.searchLogsTableWidget.setColumnCount(0)
        self.searchLogsTableWidget.setRowCount(0)
        self.searchLogsTableWidget.setMinimumSize(1250, 1750)
        self.searchLogsLayout.addWidget(self.searchLogsTableWidget)
        self.intializeText()
        self.updateLogTable()

    def intializeText(self):
        self.keywordSearchLabel.setText("Keyword Search:")
        self.creatorSearchLabel.setText("Creator:")
        self.creatorBlueTeamCheckBox.setText("Blue Team")
        self.creatorWhiteTeamCheckBox.setText("White Team")
        self.creatorRedTeamCheckBox.setText("Red Team")
        self.eventTypeBlueTeamCheckBox.setText("Blue Team")
        self.eventTypeWhiteTeamCheckBox.setText("White Team")
        self.eventTypeRedTeamCheckBox.setText("Red Team")
        self.eventTypeSearchLabel.setText("Event Type:")
        self.locationSearchLabel.setText("Location:")
        self.fromSearchLabel.setText("Start Timestamp:")
        self.toSearchLabel.setText("End Timestamp:")
        self.searchButton.setText("Apply Filter")
        self.filterConfigurationLabel.setText("FILTER CONFIGURATION")
        self.logEntryConfigurationLabel.setText("LOG ENTRY CONFIGURATION")

    def searchTableDoubleClicked(self):
        logEntryId = self.searchLogsTableWidget.verticalHeaderItem(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        logEntry = self.clientHandler.logEntryManager.logEntries[int(logEntryId)]
        logEntryDescriptionWidget = self.searchLogsTableWidget.item(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Content"))
        logEntryLocationWidget = self.searchLogsTableWidget.item(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Location"))
        associatedVectorsWidget = self.searchLogsTableWidget.cellWidget(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Vectors"))
        self.editPopup = LogEntryPopup(logEntry, logEntryDescriptionWidget, logEntryLocationWidget, associatedVectorsWidget, self.clientHandler)
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
            self.searchLogsTableWidget.setColumnWidth(colNum, 200)
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            self.searchLogsTableWidget.setHorizontalHeaderItem(colNum, QTableWidgetItem(self.colsSearchLogsTable[colNum]))
        for rowNum in range(totalRows):
            logEntryIdItem = QtWidgets.QTableWidgetItem(str(logEntries[rowNum].id))
            self.searchLogsTableWidget.setVerticalHeaderItem(rowNum, logEntryIdItem)
            self.searchLogsTableWidget.setRowHeight(rowNum, 50)
            logEntryDescriptionItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].description)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Content"), logEntryDescriptionItem)
            logEntryTeamItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].creator)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Creator"), logEntryTeamItem)
            logEntryArtifactItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].artifact)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Artifact"), logEntryArtifactItem)
            logEntryEventTypeItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].eventType)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Event Type"), logEntryEventTypeItem)
            # Populate Location column
            logEntryLocationItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].location)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Location"), logEntryLocationItem)
            # End populate Location column
            logEntryDateItem = QtWidgets.QTableWidgetItem(logEntries[rowNum].date)
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
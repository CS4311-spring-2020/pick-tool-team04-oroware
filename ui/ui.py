import copy

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QTableWidgetItem, QVBoxLayout, QFileDialog

from AddIconPopup import AddIconPopup
from GraphWidget import GraphWidget
import sys
import datetime
import xlwt

from Icon import Icon
from LogEntry import LogEntry
from LogEntryPopup import LogEntryPopup
from ClientHandler import ClientHandler
from LogEntryViewPopup import LogEntryViewPopup
from RelationshipPopup import RelationshipPopup
from SignificantEventPopup import SignificantEventPopup


class Ui_PICK(object):

    def setupMainWindow(self, PICK):
        self.mainWindow = QtWidgets.QWidget(PICK)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainWindow)

    def setupTabWidget(self):
        self.tabWidget = QtWidgets.QTabWidget(self.mainWindow)

    def setupTeamTab(self):
        self.teamConfigurationTab = QtWidgets.QWidget()
        self.teamConfigurationTabLayout = QtWidgets.QVBoxLayout(self.teamConfigurationTab)

        # Initialize Team Configuration
        self.teamConfiguration = QtWidgets.QFrame(self.teamConfigurationTab)
        self.teamConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        self.teamConfigurationLayout = QtWidgets.QVBoxLayout(self.teamConfiguration)
        self.teamConfigurationLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.teamConfigurationLabel)
        self.leadCheckBox = QtWidgets.QCheckBox(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.leadCheckBox)
        self.leadLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.leadLabel)
        self.leadTextEdit = QtWidgets.QTextEdit(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.leadTextEdit)
        self.establishedConnectionsLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.establishedConnectionsLabel)
        self.numConnectionsLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.numConnectionsLabel)
        self.connectButton = QtWidgets.QPushButton(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.connectButton)
        self.teamConfigurationTabLayout.addWidget(self.teamConfiguration)

        # Initialize Event Configuration
        self.eventConfiguration = QtWidgets.QFrame(self.teamConfigurationTab)
        self.eventConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        self.eventConfigurationLayout = QtWidgets.QVBoxLayout(self.eventConfiguration)
        self.eventConfigurationLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventConfigurationLabel)
        self.eventNameLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventNameLabel)
        self.eventNameTextEdit = QtWidgets.QTextEdit(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventNameTextEdit)
        self.eventDescriptionLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventDescriptionLabel)
        self.eventDescriptionTextEdit = QtWidgets.QTextEdit(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventDescriptionTextEdit)
        self.startEventConfigurationLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.startEventConfigurationLabel)
        self.startEventConfigurationDateEdit = QtWidgets.QDateTimeEdit(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.startEventConfigurationDateEdit)
        self.endEventConfigurationLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.endEventConfigurationLabel)
        self.endEventConfigurationDateEdit = QtWidgets.QDateTimeEdit(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.endEventConfigurationDateEdit)
        self.teamConfigurationTabLayout.addWidget(self.eventConfiguration)
        self.saveEventButton = QtWidgets.QPushButton(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.saveEventButton)

        # Intialize Ingestion Tab
        self.tabWidget.addTab(self.teamConfigurationTab, "")

    def setupDirectoryTab(self):
        self.directoryTab = QtWidgets.QWidget()
        self.directoryTabLayout = QtWidgets.QVBoxLayout(self.directoryTab)

        # Intialize Directory Configuration
        self.rootConfiguration = QtWidgets.QFrame(self.directoryTab)
        self.rootConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        self.rootConfigurationLayout = QtWidgets.QVBoxLayout(self.rootConfiguration)
        self.directoryConfigurationLabel = QtWidgets.QLabel(self.rootConfiguration)
        self.rootConfigurationLayout.addWidget(self.directoryConfigurationLabel)
        self.rootLabel = QtWidgets.QLabel(self.rootConfiguration)
        self.rootConfigurationLayout.addWidget(self.rootLabel)
        self.rootDialog = QFileDialog()
        self.rootDialog.setFileMode(QFileDialog.DirectoryOnly)
        self.rootConfigurationLayout.addWidget(self.rootDialog)
        self.directoryTabLayout.addWidget(self.rootConfiguration)

        self.redTeamConfiguration = QtWidgets.QFrame(self.directoryTab)
        self.redTeamConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        self.redTeamConfigurationLayout = QtWidgets.QVBoxLayout(self.redTeamConfiguration)
        self.redTeamLabel = QtWidgets.QLabel(self.redTeamConfiguration)
        self.redTeamConfigurationLayout.addWidget(self.redTeamLabel)
        self.redTeamDialog = QFileDialog()
        self.redTeamDialog.setFileMode(QFileDialog.DirectoryOnly)
        self.redTeamConfigurationLayout.addWidget(self.redTeamDialog)
        self.directoryTabLayout.addWidget(self.redTeamConfiguration)

        self.blueTeamConfiguration = QtWidgets.QFrame(self.directoryTab)
        self.blueTeamConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        self.blueTeamConfigurationLayout = QtWidgets.QVBoxLayout(self.blueTeamConfiguration)
        self.blueTeamLabel = QtWidgets.QLabel(self.blueTeamConfiguration)
        self.blueTeamConfigurationLayout.addWidget(self.blueTeamLabel)
        self.blueTeamDialog = QFileDialog()
        self.blueTeamDialog.setFileMode(QFileDialog.DirectoryOnly)
        self.blueTeamConfigurationLayout.addWidget(self.blueTeamDialog)
        self.directoryTabLayout.addWidget(self.blueTeamConfiguration)

        self.whiteTeamConfiguration = QtWidgets.QFrame(self.directoryTab)
        self.whiteTeamConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        self.whiteTeamConfigurationLayout = QtWidgets.QVBoxLayout(self.whiteTeamConfiguration)
        self.whiteTeamLabel = QtWidgets.QLabel(self.whiteTeamConfiguration)
        self.whiteTeamConfigurationLayout.addWidget(self.whiteTeamLabel)
        self.whiteTeamDialog = QFileDialog()
        self.whiteTeamDialog.setFileMode(QFileDialog.DirectoryOnly)
        self.whiteTeamConfigurationLayout.addWidget(self.whiteTeamDialog)
        self.ingestionButton = QtWidgets.QPushButton(self.whiteTeamConfiguration)
        self.whiteTeamConfigurationLayout.addWidget(self.ingestionButton)
        self.directoryTabLayout.addWidget(self.whiteTeamConfiguration)

        # Intialize Ingestion Tab
        self.tabWidget.addTab(self.directoryTab, "")


    def handleVectorComboBoxConfiguration(self, index):
        if self.vectorComboBoxConfiguration.count() > 0:
            self.configurationVectorDescriptionTextEdit.setPlainText(self.clientHandler.vectorManager.vectors[index.data()].vectorDescription)

    def handleVectorComboBoxTable(self, index):
        if self.vectorComboBoxTable.count() > 0:
            currentVector = self.clientHandler.vectorManager.vectors[index.data()]
            self.updateVectorTable(currentVector)
            self.updateRelationshipTable(currentVector)
            self.updateVectorGraph(currentVector)

    def setupSearchLogsTab(self):
        self.searchLogsTab = QtWidgets.QWidget()
        self.searchLogsLayout = QtWidgets.QVBoxLayout(self.searchLogsTab)
        self.filterConfigurationLabel = QtWidgets.QLabel(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.filterConfigurationLabel)
        self.keywordSearchLabel = QtWidgets.QLabel(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.keywordSearchLabel)
        self.commandSearchTextEdit = QtWidgets.QPlainTextEdit(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.commandSearchTextEdit)
        self.creatorSearchLabel = QtWidgets.QLabel(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.creatorSearchLabel)
        self.creatorBlueTeamCheckBox = QtWidgets.QCheckBox(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.creatorBlueTeamCheckBox)
        self.creatorWhiteTeamCheckBox = QtWidgets.QCheckBox(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.creatorWhiteTeamCheckBox)
        self.creatorRedTeamCheckBox = QtWidgets.QCheckBox(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.creatorRedTeamCheckBox)
        self.eventTypeSearchLabel = QtWidgets.QLabel(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.eventTypeSearchLabel)
        self.eventTypeBlueTeamCheckBox = QtWidgets.QCheckBox(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.eventTypeBlueTeamCheckBox)
        self.eventTypeWhiteTeamCheckBox = QtWidgets.QCheckBox(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.eventTypeWhiteTeamCheckBox)
        self.eventTypeRedTeamCheckBox = QtWidgets.QCheckBox(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.eventTypeRedTeamCheckBox)
        self.fromSearchLabel = QtWidgets.QLabel(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.fromSearchLabel)
        self.fromDateTimeEditSearchLogs = QtWidgets.QDateTimeEdit(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.fromDateTimeEditSearchLogs)
        self.toSearchLabel = QtWidgets.QLabel(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.toSearchLabel)
        self.toDateTimeEditSearchLogs = QtWidgets.QDateTimeEdit(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.toDateTimeEditSearchLogs)
        self.searchButton = QtWidgets.QPushButton(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.searchButton)
        # Connects Apply Filter button to method handleSearchButtonClicked
        self.searchButton.clicked.connect(self.handleSearchButtonClicked)
        self.logEntryConfigurationLabel = QtWidgets.QLabel(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.logEntryConfigurationLabel)
        self.searchLogsTableWidget = QtWidgets.QTableWidget(self.searchLogsTab)
        self.searchLogsTableWidget.setColumnCount(0)
        self.searchLogsTableWidget.setRowCount(0)
        self.searchLogsTableWidget.setMinimumSize(1250, 1750)
        self.searchLogsLayout.addWidget(self.searchLogsTableWidget)
        self.tabWidget.addTab(self.searchLogsTab, "")

    def handleSearchButtonClicked(self):
        validLogEntries = list()
        for logEntryId, logEntry in self.clientHandler.logEntryManager.logEntries.items():
            valid = True
            if not (self.commandSearchTextEdit.toPlainText() in logEntry.description):
                valid = False
            if self.creatorBlueTeamCheckBox.isChecked() and ("Blue" not in logEntry.creator):
                valid = False
            if self.creatorWhiteTeamCheckBox.isChecked() and ("White" not in logEntry.creator):
                valid = False
            if self.creatorRedTeamCheckBox.isChecked() and ("Red" not in logEntry.creator):
                valid = False
            if self.eventTypeBlueTeamCheckBox.isChecked() and ("Blue" not in logEntry.eventType):
                valid = False
            if self.eventTypeWhiteTeamCheckBox.isChecked() and ("White" not in logEntry.eventType):
                valid = False
            if self.eventTypeRedTeamCheckBox.isChecked() and ("Red" not in logEntry.eventType):
                valid = False
            if self.fromDateTimeEditSearchLogs.text() < self.startEventConfigurationDateEdit.text():
                valid = False
            if self.toDateTimeEditSearchLogs.text() > self.endEventConfigurationDateEdit.text():
                valid = False

            if(valid):
                validLogEntries.append(logEntry)
        self.clientHandler.logEntryManager.logEntriesInTable = validLogEntries
        self.updateLogTable()

    def setupVectorDbTab(self):
        self.vectorDbTab = QtWidgets.QWidget()
        self.vectorDbLayout = QtWidgets.QVBoxLayout(self.vectorDbTab)
        self.vectorDbLabel = QtWidgets.QLabel(self.vectorDbTab)
        self.vectorDbLayout.addWidget(self.vectorDbLabel)
        if self.isLead:
            self.approvalLabel = QtWidgets.QLabel(self.vectorDbTab)
            self.vectorDbLayout.addWidget(self.approvalLabel)
            self.approvalTableWidget = QtWidgets.QTableWidget(self.vectorDbTab)
            self.approvalTableWidget.setColumnCount(0)
            self.approvalTableWidget.setRowCount(0)
            self.approvalTableWidget.setMinimumSize(1250, 1750)
            self.vectorDbLayout.addWidget(self.approvalTableWidget)
        else:
            self.connectionStatusLabel = QtWidgets.QLabel(self.vectorDbTab)
            self.vectorDbLayout.addWidget(self.connectionStatusLabel)
            self.pullTableLabel = QtWidgets.QLabel(self.vectorDbTab)
            self.vectorDbLayout.addWidget(self.pullTableLabel)
            self.pullTableWidget = QtWidgets.QTableWidget(self.vectorDbTab)
            self.pullTableWidget.setColumnCount(0)
            self.pullTableWidget.setRowCount(0)
            self.pullTableWidget.setMinimumSize(1250, 850)
            self.vectorDbLayout.addWidget(self.pullTableWidget)
            self.pullButton = QtWidgets.QPushButton(self.vectorDbTab)
            self.pullButton.clicked.connect(self.handlePull)
            self.vectorDbLayout.addWidget(self.pullButton)
            self.pushTableLabel = QtWidgets.QLabel(self.vectorDbTab)
            self.vectorDbLayout.addWidget(self.pushTableLabel)
            self.pushTableWidget = QtWidgets.QTableWidget(self.vectorDbTab)
            self.pushTableWidget.setColumnCount(0)
            self.pushTableWidget.setRowCount(0)
            self.pushTableWidget.setMinimumSize(1250, 850)
            self.vectorDbLayout.addWidget(self.pushTableWidget)
            self.pushButton = QtWidgets.QPushButton(self.vectorDbTab)
            self.vectorDbLayout.addWidget(self.pushButton)
            self.pushButton.clicked.connect(self.handlePush)
            self.vectorDbLayout.addWidget(self.pushButton)
        self.tabWidget.addTab(self.vectorDbTab, "")

    def handlePull(self):
        self.clientHandler.pullVectorDb()
        self.pulledVectorManager = copy.deepcopy(self.clientHandler.vectorManager)
        self.updatePullTable(self.pulledVectorManager)
        self.updateVectorComboBoxes()
        self.updateLogTable()
        self.updateVectorConfigurationTable()
        if self.vectorComboBoxTable.count() > 0:
            self.vectorDescriptionLabel.setText("Vector Description: " + self.clientHandler.vectorManager.vectors[self.vectorComboBoxTable.itemText(0)].vectorDescription)
        if self.vectorComboBoxConfiguration.count() > 0:
            self.configurationVectorDescriptionTextEdit.setPlainText(self.clientHandler.vectorManager.vectors[self.vectorComboBoxConfiguration.itemText(0)].vectorDescription)
        self.pullButton.clicked.disconnect(self.handlePull)

    def handlePush(self):
        self.pushedVectorManager = copy.deepcopy(self.clientHandler.vectorManager)
        self.updatePushTable(self.pushedVectorManager)

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
            logEntryTeamItem = QtWidgets.QTableWidgetItem(self.clientHandler.logEntryManager.logEntries[rowNum].creator)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Creator"), logEntryTeamItem)
            logEntryArtifactItem = QtWidgets.QTableWidgetItem(self.clientHandler.logEntryManager.logEntries[rowNum].artifact)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Artifact"), logEntryArtifactItem)
            logEntryEventTypeItem = QtWidgets.QTableWidgetItem(self.clientHandler.logEntryManager.logEntries[rowNum].eventType)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Event Type"), logEntryEventTypeItem)
            logEntryDateItem = QtWidgets.QTableWidgetItem(self.clientHandler.logEntryManager.logEntries[rowNum].date)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Timestamp"), logEntryDateItem)
            logEntries[rowNum].rowIndexInTable = rowNum
            vectorComboBoxSearchTable = CheckableComboBox(logEntries[rowNum])
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

    def updateVectorConfigurationTable(self):
        vectors = self.clientHandler.vectorManager.vectors
        totalRows = len(vectors)
        self.vectorConfigurationTableWidget.setColumnCount(len(self.colsVectorConfigurationTable))
        self.vectorConfigurationTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.vectorConfigurationTableWidget.setRowCount(totalRows)
        header = self.vectorConfigurationTableWidget.horizontalHeader()
        for colNum in range(len(self.colsVectorConfigurationTable)):
            self.vectorConfigurationTableWidget.setColumnWidth(colNum, 200)
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            self.vectorConfigurationTableWidget.setHorizontalHeaderItem(colNum,
                                                               QTableWidgetItem(self.colsVectorConfigurationTable[colNum]))
        rowNum = 0
        for vectorName, vector in vectors.items():
            self.vectorConfigurationTableWidget.setRowHeight(rowNum, 50)
            vectorNameItem = QtWidgets.QTableWidgetItem(vectorName)
            self.vectorConfigurationTableWidget.setItem(rowNum, self.colsVectorConfigurationTable.index("Vector Name"), vectorNameItem)
            vectorDescriptionItem = QtWidgets.QTableWidgetItem(vector.vectorDescription)
            self.vectorConfigurationTableWidget.setItem(rowNum, self.colsVectorConfigurationTable.index("Vector Description"), vectorDescriptionItem)
            rowNum += 1
        self.vectorConfigurationTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def updatePullTable(self, pulledVectorManager):
        vectors = pulledVectorManager.vectors
        totalRows = len(vectors)
        self.pullTableWidget.setColumnCount(len(self.colsPullTable))
        self.pullTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.pullTableWidget.setRowCount(totalRows)
        header = self.pullTableWidget.horizontalHeader()
        for colNum in range(len(self.colsPullTable)):
            self.pullTableWidget.setColumnWidth(colNum, 200)
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            self.pullTableWidget.setHorizontalHeaderItem(colNum, QTableWidgetItem(self.colsPullTable[colNum]))
        rowNum = 0
        for vectorName, vector in vectors.items():
            self.pullTableWidget.setRowHeight(rowNum, 50)
            vectorNameItem = QtWidgets.QTableWidgetItem(vectorName)
            self.pullTableWidget.setItem(rowNum, self.colsPullTable.index("Vector Name"), vectorNameItem)
            vectorDescriptionItem = QtWidgets.QTableWidgetItem(vector.vectorDescription)
            self.pullTableWidget.setItem(rowNum, self.colsPullTable.index("Vector Description"), vectorDescriptionItem)
            graphButton = ViewGraphButton(vector)
            graphButton.setText("View Graph")
            self.pullTableWidget.setCellWidget(rowNum, self.colsPullTable.index("Vector Graph"), graphButton)
            rowNum += 1
        self.pushTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def updatePushTable(self, pushedVectorManager):
        vectors = pushedVectorManager.vectors
        totalRows = len(vectors)
        self.pushTableWidget.setColumnCount(len(self.colsPushTable))
        self.pushTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.pushTableWidget.setRowCount(totalRows)
        header = self.pushTableWidget.horizontalHeader()
        for colNum in range(len(self.colsPushTable)):
            self.pushTableWidget.setColumnWidth(colNum, 200)
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            self.pushTableWidget.setHorizontalHeaderItem(colNum, QTableWidgetItem(self.colsPushTable[colNum]))
        rowNum = 0
        for vectorName, vector in vectors.items():
            self.pushTableWidget.setRowHeight(rowNum, 50)
            vectorNameItem = QtWidgets.QTableWidgetItem(vectorName)
            self.pushTableWidget.setItem(rowNum, self.colsPushTable.index("Vector Name"), vectorNameItem)
            vectorDescriptionItem = QtWidgets.QTableWidgetItem(vector.vectorDescription)
            self.pushTableWidget.setItem(rowNum, self.colsPushTable.index("Vector Description"), vectorDescriptionItem)
            graphButton = ViewGraphButton(vector)
            graphButton.setText("View Graph")
            self.pushTableWidget.setCellWidget(rowNum, self.colsPushTable.index("Vector Graph"), graphButton)
            rowNum += 1
        self.pushTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def updateApproveTable(self, pushedVectors, pushedIps, pushedTimestamps, changeSummaries):
        self.colsApproveTable = ["Source IP", "Request Timestamp", "Vector Name", "Vector Description", "Graph", "Change Summary", "Approve"]
        totalRows = len(pushedVectors)
        self.approvalTableWidget.setColumnCount(len(self.colsApproveTable))
        self.approvalTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.approvalTableWidget.setRowCount(totalRows)
        header = self.approvalTableWidget.horizontalHeader()
        for colNum in range(len(self.colsApproveTable)):
            self.approvalTableWidget.setColumnWidth(colNum, 200)
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            self.approvalTableWidget.setHorizontalHeaderItem(colNum, QTableWidgetItem(self.colsApproveTable[colNum]))
        for rowNum in range(pushedVectors):
            self.approvalTableWidget.setRowHeight(rowNum, 50)
            vectorNameItem = QtWidgets.QTableWidgetItem(pushedVectors[rowNum].vectorName)
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Vector Name"), vectorNameItem)
            changeItem = QtWidgets.QTableWidgetItem(changeSummaries[rowNum])
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Change Summary"), changeItem)
            timestampItem = QtWidgets.QTableWidgetItem(pushedTimestamps[rowNum])
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Request Timestamp"), timestampItem)
            sourceItem = QtWidgets.QTableWidgetItem(pushedIps[rowNum])
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Source IP"), sourceItem)
            vectorDescriptionItem = QtWidgets.QTableWidgetItem(pushedVectors[rowNum].vectorDescription)
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Vector Description"), vectorDescriptionItem)
            graphButton = QtWidgets.QPushButton()
            graphButton.setText("View Graph")
            self.approvalTableWidget.setCellWidget(rowNum, self.colsApproveTable.index("Vector Graph"), graphButton)
            approveButton = QtWidgets.QPushButton()
            approveButton.setText("Approve")
            self.approvalTableWidget.setCellWidget(rowNum, self.colsApproveTable.index("Approve"), approveButton)
        self.approvalTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def updateIconConfigurationTable(self):
        icons = self.clientHandler.iconManager.icons
        totalRows = len(icons)
        self.iconConfigurationTableWidget.setColumnCount(len(self.colsIconConfigurationTable))
        self.iconConfigurationTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.iconConfigurationTableWidget.setRowCount(totalRows)
        header = self.iconConfigurationTableWidget.horizontalHeader()
        for colNum in range(len(self.colsIconConfigurationTable)):
            self.iconConfigurationTableWidget.setColumnWidth(colNum, 200)
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            self.iconConfigurationTableWidget.setHorizontalHeaderItem(colNum,
                                                               QTableWidgetItem(self.colsIconConfigurationTable[colNum]))
        rowNum = 0
        for iconName, icon in icons.items():
            self.iconConfigurationTableWidget.setRowHeight(rowNum, 50)
            iconNameItem = QtWidgets.QTableWidgetItem(iconName)
            self.iconConfigurationTableWidget.setItem(rowNum, self.colsIconConfigurationTable.index("Icon Name"),
                                               iconNameItem)
            iconSourceItem = QtWidgets.QTableWidgetItem(icon.source)
            self.iconConfigurationTableWidget.setItem(rowNum, self.colsIconConfigurationTable.index("Icon Source"), iconSourceItem)
            viewIconButton = QtWidgets.QPushButton()
            viewIconButton.setText("View Icon")
            self.iconConfigurationTableWidget.setCellWidget(rowNum, self.colsIconConfigurationTable.index("Icon Preview"),
                                                     viewIconButton)
            icon.rowIndexInTable = rowNum
            rowNum += 1
        self.iconConfigurationTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def updateVectorTable(self, vector):
        significantEvents = list(vector.significantEvents.values())
        totalRows = len(significantEvents) + 1
        self.vectorTableWidget.setColumnCount(len(self.colsVectorTable))
        self.vectorTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.vectorTableWidget.setRowCount(totalRows)
        header = self.vectorTableWidget.horizontalHeader()
        for colNum in range(len(self.colsVectorTable)):
            self.vectorTableWidget.setColumnWidth(colNum, 200)
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            self.vectorTableWidget.setHorizontalHeaderItem(colNum, QTableWidgetItem(self.colsVectorTable[colNum]))
            if colNum != self.colsVectorTable.index("Icon Type") and colNum != self.colsVectorTable.index("Reference"):
                visibilityCheckbox = VisibilityCheckBox(self.colsVectorTable[colNum], vector)
                visibilityCheckbox.setCheckState(QtCore.Qt.Checked if vector.visibility[self.colsVectorTable[colNum]] else QtCore.Qt.Unchecked)
                visibilityCheckbox.setText("Visible")
                self.vectorTableWidget.setCellWidget(0, colNum, visibilityCheckbox)
        self.vectorTableWidget.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem(""))
        rowNum = 1
        while(rowNum < totalRows):
            significantEvent = significantEvents[rowNum-1]
            significantEventIdItem = QtWidgets.QTableWidgetItem(str(significantEvent.id))
            self.vectorTableWidget.setVerticalHeaderItem(rowNum, significantEventIdItem)
            self.vectorTableWidget.setRowHeight(rowNum, 50)
            significantEventTypeItem = QtWidgets.QTableWidgetItem(significantEvent.logEntry.eventType)
            logEntry = significantEvent.logEntry
            viewEntryButton = ViewReferenceButton(logEntry)
            viewEntryButton.setText("View Log Entry")
            self.vectorTableWidget.setCellWidget(rowNum, self.colsVectorTable.index("Reference"),
                                                     viewEntryButton)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Event Type"), significantEventTypeItem)
            iconComboBox = IconComboBox(significantEvent)
            iconComboBox.addItem(significantEvent.iconType)
            if Icon.DEFAULT != significantEvent.iconType:
                iconComboBox.addItem(Icon.DEFAULT)
            for iconName, icon in self.clientHandler.iconManager.icons.items():
                if iconName != significantEvent.iconType:
                    iconComboBox.addItem(iconName)
            self.vectorTableWidget.setCellWidget(rowNum, self.colsVectorTable.index("Icon Type"), iconComboBox)
            significantEventNameItem = QtWidgets.QTableWidgetItem(significantEvent.name)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Node Name"), significantEventNameItem)
            significantEventDateItem = QtWidgets.QTableWidgetItem(significantEvent.logEntry.date)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Node Timestamp"), significantEventDateItem)
            significantEventCreatorItem = QtWidgets.QTableWidgetItem(significantEvent.logEntry.creator)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Event Creator"), significantEventCreatorItem)
            significantEventDescriptionItem = QtWidgets.QTableWidgetItem(significantEvent.description)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Node Description"), significantEventDescriptionItem)
            significantEventArtifactItem = QtWidgets.QTableWidgetItem(significantEvent.logEntry.artifact)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Artifact"), significantEventArtifactItem)
            significantEvent.rowIndexInTable = rowNum
            rowNum += 1
        self.vectorTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.vectorTableWidget.doubleClicked.connect(self.vectorTableDoubleClicked)

    def updateRelationshipTable(self, vector):
        relationships = list(vector.relationships.values())
        totalRows = len(relationships)
        self.relationshipTableWidget.setColumnCount(len(self.colsRelationshipTable))
        self.relationshipTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.relationshipTableWidget.setRowCount(totalRows)
        header = self.relationshipTableWidget.horizontalHeader()
        for colNum in range(len(self.colsRelationshipTable)):
            self.relationshipTableWidget.setColumnWidth(colNum, 200)
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            self.relationshipTableWidget.setHorizontalHeaderItem(colNum, QTableWidgetItem(self.colsRelationshipTable[colNum]))
        for rowNum in range(totalRows):
            self.relationshipTableWidget.setRowHeight(rowNum, 50)
            relationshipIdItem = QtWidgets.QTableWidgetItem(str(relationships[rowNum].id))
            self.relationshipTableWidget.setVerticalHeaderItem(rowNum, relationshipIdItem)
            relationshipSourceItem = QtWidgets.QTableWidgetItem(str(relationships[rowNum].sourceSignificantEventId))
            self.relationshipTableWidget.setItem(rowNum, self.colsRelationshipTable.index("Parent"), relationshipSourceItem)
            relationshipDestItem = QtWidgets.QTableWidgetItem(str(relationships[rowNum].destSignificantEventId))
            self.relationshipTableWidget.setItem(rowNum, self.colsRelationshipTable.index("Child"), relationshipDestItem)
            relationshipDescriptionItem = QtWidgets.QTableWidgetItem(relationships[rowNum].description)
            self.relationshipTableWidget.setItem(rowNum, self.colsRelationshipTable.index("Label"), relationshipDescriptionItem)
            relationships[rowNum].rowIndexInTable = rowNum
        self.relationshipTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.relationshipTableWidget.doubleClicked.connect(self.relationshipTableDoubleClicked)

    def updateVectorGraph(self, vector):
        self.vectorGraphWidget.initializeVector(vector)
        self.vectorGraphWidget.draw()

    def viewLogEntryClicked(self, logEntry):
        self.viewPopup = LogEntryViewPopup(logEntry)
        self.viewPopup.setGeometry(100, 200, 200, 200)
        self.viewPopup.show()

    def viewGraphClicked(self, vector):
        self.viewGraphWindow = QtWidgets.QWidget()
        layout = QVBoxLayout()
        immutableGraphWidget = GraphWidget(self.viewGraphWindow, None, mutable=False)
        immutableGraphWidget.initializeVector(vector)
        immutableGraphWidget.draw()
        layout.addWidget(immutableGraphWidget)
        self.viewGraphWindow.setLayout(layout)
        self.viewGraphWindow.setWindowTitle("View Graph Popup")
        self.viewGraphWindow.setGeometry(500, 500, 600, 600)
        self.viewGraphWindow.show()

    def searchTableDoubleClicked(self):
        logEntryId = self.searchLogsTableWidget.verticalHeaderItem(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        logEntry = self.clientHandler.logEntryManager.logEntries[int(logEntryId)]
        logEntryDescriptionWidget = self.searchLogsTableWidget.item(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Content"))
        associatedVectorsWidget = self.searchLogsTableWidget.cellWidget(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Vectors"))
        self.editPopup = LogEntryPopup(logEntry, logEntryDescriptionWidget, associatedVectorsWidget, self.clientHandler)
        self.editPopup.setGeometry(100, 200, 200, 200)
        self.editPopup.show()

    def vectorTableDoubleClicked(self):
        trigger = TriggerHelper()
        significantEventId = self.vectorTableWidget.verticalHeaderItem(self.vectorTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        vectorName = self.vectorComboBoxTable.currentText()
        vector = self.clientHandler.vectorManager.vectors[vectorName]
        significantEventToEdit = vector.significantEvents[int(significantEventId)]
        self.editEventPopup = SignificantEventPopup(vector, significantEventToEdit, trigger)
        self.editEventPopup.setGeometry(100, 200, 200, 200)
        self.editEventPopup.show()

    def relationshipTableDoubleClicked(self):
        trigger = TriggerHelper()
        relationshipId = self.relationshipTableWidget.verticalHeaderItem(self.relationshipTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        vectorName = self.vectorComboBoxTable.currentText()
        vector = self.clientHandler.vectorManager.vectors[vectorName]
        relationshipToEdit = vector.relationships[int(relationshipId)]
        self.editRelationshipPopup = RelationshipPopup(vector, relationshipToEdit, trigger)
        self.editRelationshipPopup.setGeometry(100, 200, 100, 100)
        self.editRelationshipPopup.show()

    def setupEditVectorTab(self):
        self.editVectorTab = QtWidgets.QWidget()
        self.editVectorLayout = QtWidgets.QHBoxLayout(self.editVectorTab)
        self.leftEditVectorWidget = QtWidgets.QWidget(self.editVectorTab)
        self.leftEditVectorLayout = QtWidgets.QVBoxLayout(self.leftEditVectorWidget)
        self.graphWidget = QtWidgets.QWidget(self.leftEditVectorWidget)
        self.graphLayout = QtWidgets.QVBoxLayout(self.graphWidget)
        triggerHelper = TriggerHelper()
        triggerHelper.connectRelationshipTableTrigger()
        self.vectorGraphWidget = GraphWidget(self.graphWidget, triggerHelper)
        self.vectorGraphWidget.setMinimumSize(QtCore.QSize(1500, 1500))
        self.graphLayout.addWidget(self.vectorGraphWidget)
        self.graphFrame = QtWidgets.QFrame(self.graphWidget)
        self.graphFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.graphFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.filterGraphLayout = QtWidgets.QVBoxLayout(self.graphFrame)
        self.addNodeGraphButton = QtWidgets.QPushButton(self.graphFrame)
        self.addNodeGraphButton.clicked.connect(self.handleAddNode)
        self.filterGraphLayout.addWidget(self.addNodeGraphButton)
        self.zoomInButtonGraph = QtWidgets.QPushButton(self.graphFrame)
        self.zoomInButtonGraph.clicked.connect(self.vectorGraphWidget.maximize)
        self.filterGraphLayout.addWidget(self.zoomInButtonGraph)
        self.zoomOutButtonGraph = QtWidgets.QPushButton(self.graphFrame)
        self.zoomOutButtonGraph.clicked.connect(self.vectorGraphWidget.minimize)
        self.filterGraphLayout.addWidget(self.zoomOutButtonGraph)
        self.graphLayout.addWidget(self.graphFrame)
        self.leftEditVectorLayout.addWidget(self.graphWidget)
        self.editVectorLayout.addWidget(self.leftEditVectorWidget)
        self.rightEditVectorWidget = QtWidgets.QWidget(self.editVectorTab)
        self.rightEditVectorLayout = QtWidgets.QVBoxLayout(self.rightEditVectorWidget)
        self.vectorFrame = QtWidgets.QFrame(self.rightEditVectorWidget)
        self.vectorFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.vectorFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.editVectorTableLayout = QtWidgets.QVBoxLayout(self.vectorFrame)
        self.vectorTableLabel = QtWidgets.QLabel(self.vectorFrame)
        self.editVectorTableLayout.addWidget(self.vectorTableLabel)
        self.vectorComboBoxTable = QtWidgets.QComboBox(self.vectorFrame)
        self.vectorComboBoxTable.view().pressed.connect(self.handleVectorComboBoxTable)
        self.editVectorTableLayout.addWidget(self.vectorComboBoxTable)
        self.vectorDescriptionLabel = QtWidgets.QLabel(self.vectorFrame)
        self.editVectorTableLayout.addWidget(self.vectorDescriptionLabel)
        self.exportTableButton = QtWidgets.QPushButton(self.vectorFrame)
        self.exportTableButton.clicked.connect(self.handleExport)
        self.editVectorTableLayout.addWidget(self.exportTableButton)
        self.addNodeTableButton = QtWidgets.QPushButton(self.vectorFrame)
        self.addNodeTableButton.clicked.connect(self.handleAddNode)
        self.editVectorTableLayout.addWidget(self.addNodeTableButton)
        self.rightEditVectorLayout.addWidget(self.vectorFrame)
        self.nodeTableLabel = QtWidgets.QLabel(self.rightEditVectorWidget)
        self.rightEditVectorLayout.addWidget(self.nodeTableLabel)
        self.vectorTableWidget = QtWidgets.QTableWidget(self.rightEditVectorWidget)
        self.vectorTableWidget.setColumnCount(0)
        self.vectorTableWidget.setRowCount(0)
        self.rightEditVectorLayout.addWidget(self.vectorTableWidget)
        self.relationshipTableLabel = QtWidgets.QLabel(self.rightEditVectorWidget)
        self.rightEditVectorLayout.addWidget(self.relationshipTableLabel)
        self.relationshipTableWidget = QtWidgets.QTableWidget(self.rightEditVectorWidget)
        self.relationshipTableWidget.setColumnCount(0)
        self.relationshipTableWidget.setRowCount(0)
        self.rightEditVectorLayout.addWidget(self.relationshipTableWidget)
        self.editVectorLayout.addWidget(self.rightEditVectorWidget)
        self.tabWidget.addTab(self.editVectorTab, "")
        self.tabWidget.currentChanged.connect(self.onTabChange)

    def setupVectorConfigurationTab(self):
        self.vectorConfigurationTab = QtWidgets.QWidget()
        self.vectorConfigurationLayout = QtWidgets.QVBoxLayout(self.vectorConfigurationTab)
        self.vectorConfigurationLabel = QtWidgets.QLabel(self.vectorConfigurationTab)
        self.vectorConfigurationLayout.addWidget(self.vectorConfigurationLabel)
        self.currentVectorConfigurationLabel = QtWidgets.QLabel(self.vectorConfigurationTab)
        self.vectorConfigurationLayout.addWidget(self.currentVectorConfigurationLabel)
        self.vectorComboBoxConfiguration = QtWidgets.QComboBox(self.vectorConfigurationTab)
        self.vectorComboBoxConfiguration.setModel(QtGui.QStandardItemModel())
        self.vectorComboBoxConfiguration.view().pressed.connect(self.handleVectorComboBoxConfiguration)
        self.vectorConfigurationLayout.addWidget(self.vectorComboBoxConfiguration)
        self.configurationVectorDescriptionLabel = QtWidgets.QLabel(self.vectorConfigurationTab)
        self.vectorConfigurationLayout.addWidget(self.configurationVectorDescriptionLabel)
        self.configurationVectorDescriptionTextEdit = QtWidgets.QPlainTextEdit(self.vectorConfigurationTab)
        self.vectorConfigurationLayout.addWidget(self.configurationVectorDescriptionTextEdit)
        self.deleteVectorButton = QtWidgets.QPushButton(self.vectorConfigurationTab)
        self.vectorConfigurationLayout.addWidget(self.deleteVectorButton)
        self.editVectorButton = QtWidgets.QPushButton(self.vectorConfigurationTab)
        self.vectorConfigurationLayout.addWidget(self.editVectorButton)
        self.addVectorButton = QtWidgets.QPushButton(self.vectorConfigurationTab)
        self.vectorConfigurationLayout.addWidget(self.addVectorButton)
        self.vectorConfigurationTableWidget = QtWidgets.QTableWidget(self.vectorConfigurationTab)
        self.vectorConfigurationTableWidget.setColumnCount(0)
        self.vectorConfigurationTableWidget.setRowCount(0)
        self.vectorConfigurationTableWidget.setMinimumSize(1250, 1750)
        self.vectorConfigurationLayout.addWidget(self.vectorConfigurationTableWidget)
        self.tabWidget.addTab(self.vectorConfigurationTab, "")

    def setupIconConfigurationTab(self):
        self.iconConfigurationTab = QtWidgets.QWidget()
        self.iconConfigurationLayout = QtWidgets.QVBoxLayout(self.iconConfigurationTab)
        self.iconConfigurationLabel = QtWidgets.QLabel(self.iconConfigurationTab)
        self.iconConfigurationLayout.addWidget(self.iconConfigurationLabel)
        self.addIconButton = QtWidgets.QPushButton(self.iconConfigurationTab)
        self.addIconButton.clicked.connect(self.handleAddIcon)
        self.iconConfigurationLayout.addWidget(self.addIconButton)
        self.iconConfigurationTableWidget = QtWidgets.QTableWidget(self.iconConfigurationTab)
        self.iconConfigurationTableWidget.setColumnCount(0)
        self.iconConfigurationTableWidget.setRowCount(0)
        self.iconConfigurationTableWidget.setMinimumSize(1250, 1750)
        self.iconConfigurationLayout.addWidget(self.iconConfigurationTableWidget)
        self.tabWidget.addTab(self.iconConfigurationTab, "")

    def handleAddIcon(self):
        triggerHelper = TriggerHelper()
        self.addIconPopup = AddIconPopup(triggerHelper, self.clientHandler)
        self.addIconPopup.setGeometry(100, 200, 200, 200)
        self.addIconPopup.show()

    def handleExport(self):
        if self.vectorComboBoxTable.count() > 0:
            self.vectorGraphWidget.export()
            self.exportVectorTable(self.vectorComboBoxTable.currentText())
            self.exportRelationshipTable(self.vectorComboBoxTable.currentText())

    def handleVectorTableEntryUpdate(self, significantEvent, vectorName):
        if significantEvent.rowIndexInTable != -1 and self.vectorComboBoxTable.count() > 0 and self.vectorComboBoxTable.currentText() == vectorName:
            significantEventDescriptionItem = QtWidgets.QTableWidgetItem(significantEvent.logEntry.description)
            self.vectorTableWidget.setItem(significantEvent.rowIndexInTable, len(self.colsVectorTable) - 1,
                                                   significantEventDescriptionItem)

    def handleSearchLogTableEntryUpdate(self, logEntry):
        if logEntry.rowIndexInTable != -1:
            logEntryDescriptionItem = QtWidgets.QTableWidgetItem(logEntry.description)
            self.searchLogsTableWidget.setItem(logEntry.rowIndexInTable, self.colsSearchLogsTable.index("Content"),
                                                   logEntryDescriptionItem)

    def handleRelationshipTableEntryUpdate(self, relationship, vectorName):
        if relationship.rowIndexInTable != -1 and self.vectorComboBoxTable.count() > 0 and self.vectorComboBoxTable.currentText() == vectorName:
            relationshipDescriptionItem = QtWidgets.QTableWidgetItem(relationship.description)
            self.relationshipTableWidget.setItem(relationship.rowIndexInTable, self.colsRelationshipTable.index("Label"),
                                                   relationshipDescriptionItem)

    def exportVectorTable(self, vectorName):
        filename = vectorName + "_SignificantEventTable.xls"
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.vectorTableWidget.model()
        for column in range(model.columnCount()):
            text = model.headerData(column, QtCore.Qt.Horizontal)
            sheet.write(0, column + 1, text, style=style)
        for row in range(model.rowCount()):
            text = model.headerData(row, QtCore.Qt.Vertical)
            sheet.write(row + 1, 0, text, style=style)
        for column in range(model.columnCount()):
            for row in range(model.rowCount()):
                text = model.data(model.index(row, column))
                sheet.write(row + 1, column + 1, text)
        wbk.save(filename)

    def exportRelationshipTable(self, vectorName):
        filename = vectorName + "_RelationshipTable.xls"
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.relationshipTableWidget.model()
        for column in range(model.columnCount()):
            text = model.headerData(column, QtCore.Qt.Horizontal)
            sheet.write(0, column + 1, text, style=style)
        for row in range(model.rowCount()):
            text = model.headerData(row, QtCore.Qt.Vertical)
            sheet.write(row + 1, 0, text, style=style)
        for column in range(model.columnCount()):
            for row in range(model.rowCount()):
                text = model.data(model.index(row, column))
                sheet.write(row + 1, column + 1, text)
        wbk.save(filename)

    def handleAddNode(self):
        if self.vectorComboBoxTable.count() > 0:
            vectorName = self.vectorComboBoxTable.currentText()
            vector = self.clientHandler.vectorManager.vectors[vectorName]
            logEntry = LogEntry()
            logEntry.creator = logEntry.WHITE_TEAM
            logEntry.eventType = logEntry.WHITE_TEAM
            logEntry.id = self.clientHandler.logEntryManager.nextAvailableId
            self.clientHandler.logEntryManager.nextAvailableId += 1
            logEntry.date = (datetime.datetime.today()).strftime("%m/%d/%Y %I:%M %p").lstrip("0")
            logEntry.associatedVectors.append(self.vectorComboBoxTable.currentText())
            vector.addSignificantEventFromLogEntry(logEntry)
            self.updateVectorTable(vector)
            self.updateVectorGraph(vector)

    def onTabChange(self):
        if self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.editVectorTab) and self.vectorComboBoxTable.count() > 0:
            self.graphLayout.removeWidget(self.vectorGraphWidget)
            triggerHelper = TriggerHelper()
            triggerHelper.connectRelationshipTableTrigger()
            self.vectorGraphWidget = GraphWidget(self.graphWidget, triggerHelper)
            self.vectorGraphWidget.setMinimumSize(QtCore.QSize(1500, 1500))
            self.graphLayout.addWidget(self.vectorGraphWidget)
            self.zoomInButtonGraph.clicked.disconnect()
            self.zoomOutButtonGraph.clicked.disconnect()
            self.zoomInButtonGraph.clicked.connect(self.vectorGraphWidget.maximize)
            self.zoomOutButtonGraph.clicked.connect(self.vectorGraphWidget.minimize)
            vectorName = self.vectorComboBoxTable.currentText()
            vector = self.clientHandler.vectorManager.vectors[vectorName]
            self.updateVectorTable(vector)
            self.updateRelationshipTable(vector)
            self.updateVectorGraph(vector)

    def handleRelationshipTableTrigger(self):
        if self.vectorComboBoxTable.count() > 0:
            vectorName = self.vectorComboBoxTable.currentText()
            vector = self.clientHandler.vectorManager.vectors[vectorName]
            self.updateRelationshipTable(vector)

    def handleVectorGraphTrigger(self):
        if self.vectorComboBoxTable.count() > 0:
            vectorName = self.vectorComboBoxTable.currentText()
            vector = self.clientHandler.vectorManager.vectors[vectorName]
            self.updateVectorGraph(vector)

    def updateVectorComboBoxes(self):
        vectorNames = (self.clientHandler.vectorManager.vectors.keys())
        self.vectorComboBoxTable.clear()
        self.vectorComboBoxConfiguration.clear()
        for vectorName in vectorNames:
            self.vectorComboBoxTable.addItem(vectorName)
            self.vectorComboBoxConfiguration.addItem(vectorName)

    def setupUi(self, PICK):
        PICK.resize(3500, 2000)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PICK.sizePolicy().hasHeightForWidth())
        PICK.setSizePolicy(sizePolicy)
        PICK.setMaximumSize(QtCore.QSize(16777215, 3000))
        PICK.setMinimumSize(QtCore.QSize(0, 900))

        self.establishedConnections = 0
        self.numConnections = 0
        self.isLead = False
        self.connectionStatus = True

        # Table column names
        self.colsSearchLogsTable = ["Timestamp", "Content", "Artifact", "Creator", "Event Type", "Vectors"]
        self.colsVectorConfigurationTable = ["Vector Name", "Vector Description"]
        self.colsIconConfigurationTable = ["Icon Name", "Icon Source", "Icon Preview"]
        self.colsVectorTable = ["Node Name", "Node Timestamp", "Node Description", "Reference", "Event Creator", "Event Type", "Icon Type", "Artifact"]
        self.colsRelationshipTable = ["Parent", "Child", "Label"]
        self.colsPullTable = ["Vector Name", "Vector Description", "Vector Graph"]
        self.colsPushTable = ["Vector Name", "Vector Description", "Vector Graph"]
        self.colsApproveTable = ["Source IP", "Request Timestamp", "Vector Name", "Vector Description", "Graph", "Approve"]

        self.clientHandler = ClientHandler()

        # Vector list
        self.vectors = list()
        # Initialization of vector list
        self.vectors = list(self.clientHandler.vectorManager.vectors.values())

        self.setupMainWindow(PICK)
        self.setupTabWidget()
        self.setupTeamTab()
        self.setupDirectoryTab()
        self.setupSearchLogsTab()
        self.setupVectorConfigurationTab()
        self.setupIconConfigurationTab()
        self.clientHandler.logEntryManager.searchLogEntryTableWidget = self.searchLogsTableWidget
        self.clientHandler.logEntryManager.colNamesInSearchLogsTable = self.colsSearchLogsTable
        self.updateLogTable()
        self.updateVectorConfigurationTable()
        self.updateIconConfigurationTable()
        self.setupEditVectorTab()
        self.setupVectorDbTab()
        self.updateVectorComboBoxes()
        if self.vectorComboBoxTable.count() > 0:
            self.vectorDescriptionLabel.setText("Vector Description: " + self.clientHandler.vectorManager.vectors[self.vectorComboBoxTable.itemText(0)].vectorDescription)
        if self.vectorComboBoxConfiguration.count() > 0:
            self.configurationVectorDescriptionTextEdit.setPlainText(self.clientHandler.vectorManager.vectors[self.vectorComboBoxConfiguration.itemText(0)].vectorDescription)
        self.verticalLayout.addWidget(self.tabWidget)
        PICK.setCentralWidget(self.mainWindow)
        self.setAllText(PICK)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PICK)

    def setAllText(self, PICK):
        PICK.setWindowTitle("PICK Tool")
        self.vectorConfigurationLabel.setText("VECTOR CONFIGURATION")
        self.addVectorButton.setText("Add Vector")
        self.addIconButton.setText("Add Icon")
        self.deleteVectorButton.setText("Delete Vector")
        self.editVectorButton.setText("Edit Vector")
        self.exportTableButton.setText("Export Vector")
        self.teamConfigurationLabel.setText("TEAM CONFIGURATION")
        self.teamConfigurationLabel.setText("TEAM CONFIGURATION")
        self.vectorDbLabel.setText("VECTOR DB CONFIGURATION")
        if self.isLead:
            self.approvalLabel.setText("Approval sync:")
        else:
            self.pullTableLabel.setText("Pulled Vector DB Table (Analyst):")
            self.pushTableLabel.setText("Pushed Vector DB Table (Analyst):")
            self.connectionStatusLabel.setText("Connected with lead: " + str(self.connectionStatus))
            self.pushButton.setText("Push Button")
            self.pullButton.setText("Pull Button")
        self.eventConfigurationLabel.setText("EVENT CONFIGURATION")
        self.leadCheckBox.setText("Lead")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.teamConfigurationTab), "Team and Event Configuration")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.vectorConfigurationTab), "Vector Configuration")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.iconConfigurationTab), "Icon Configuration")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.directoryTab), "Directory Configuration")
        self.keywordSearchLabel.setText("Keyword Search:")
        self.creatorSearchLabel.setText("Creator:")
        self.creatorBlueTeamCheckBox.setText("Blue Team")
        self.creatorWhiteTeamCheckBox.setText("White Team")
        self.creatorRedTeamCheckBox.setText("Red Team")
        self.eventTypeBlueTeamCheckBox.setText("Blue Team")
        self.eventTypeWhiteTeamCheckBox.setText("White Team")
        self.eventTypeRedTeamCheckBox.setText("Red Team")
        self.eventTypeSearchLabel.setText("Event Type:")
        self.fromSearchLabel.setText("Start Timestamp:")
        self.eventConfigurationLabel.setText("EVENT CONFIGURATION")
        self.iconConfigurationLabel.setText("ICON CONFIGURATION")
        self.toSearchLabel.setText("End Timestamp:")
        self.redTeamLabel.setText("Red Team Folder: ")
        self.searchButton.setText("Apply Filter")
        self.currentVectorConfigurationLabel.setText("Current vector:")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.searchLogsTab), "Search Logs")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.vectorDbTab), "Vector DB Configuration")
        self.addNodeGraphButton.setText("Add Node")
        self.leadCheckBox.setText("Lead: ")
        self.filterConfigurationLabel.setText("FILTER CONFIGURATION")
        self.rootLabel.setText("Root Directory: ")
        self.leadLabel.setText("Lead's IP Address: ")
        self.zoomInButtonGraph.setText("Zoom In")
        self.zoomOutButtonGraph.setText("Zoom Out")
        self.eventNameLabel.setText("Event name: ")
        self.whiteTeamLabel.setText("White Team Folder: ")
        self.connectButton.setText("Connect")
        self.startEventConfigurationLabel.setText("Event start timestamp:")
        self.directoryConfigurationLabel.setText("DIRECTORY CONFIGURATION")
        self.vectorTableLabel.setText("Vector:")
        self.configurationVectorDescriptionLabel.setText("Vector Description:")
        self.logEntryConfigurationLabel.setText("LOG ENTRY CONFIGURATION")
        self.saveEventButton.setText("Save Event")
        self.ingestionButton.setText("Start Data Ingestion")
        self.eventDescriptionLabel.setText("Event description: ")
        self.addNodeTableButton.setText("Add Node")
        self.establishedConnectionsLabel.setText("No. of established connections to the lead’s IP address: " + str(self.establishedConnections))
        self.numConnectionsLabel.setText("No. of connections to the lead’s IP address: " + str(self.numConnections))
        self.endEventConfigurationLabel.setText("Event end timestamp:")
        self.blueTeamLabel.setText("Blue Team Folder: ")
        self.nodeTableLabel.setText("Nodes:")
        self.relationshipTableLabel.setText("Relationships:")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.editVectorTab), "Edit Vector")

class TriggerHelper(QObject):
    updateRelationshipTableTrigger = pyqtSignal()
    updateVectorGraphTrigger = pyqtSignal()
    updateVectorTableEntryTrigger = pyqtSignal()
    updateSearchLogTableEntryTrigger = pyqtSignal()
    updateRelationshipTableEntryTrigger = pyqtSignal()
    updateVectorTableTrigger = pyqtSignal()
    updateIconTableTrigger = pyqtSignal()

    def connectRelationshipTableTrigger(self):
        self.updateRelationshipTableTrigger.connect(ui.handleRelationshipTableTrigger)

    def connectIconTableTrigger(self):
        self.updateIconTableTrigger.connect(ui.updateIconConfigurationTable)

    def connectVectorGraphTrigger(self):
        self.updateVectorGraphTrigger.connect(ui.handleVectorGraphTrigger)

    def connectVectorTableTrigger(self):
        self.updateVectorTableTrigger.connect(ui.onTabChange)

    def connectVectorTableEntryTrigger(self, significantEvent, vectorName):
        self.updateVectorTableEntryTrigger.connect(lambda: ui.handleVectorTableEntryUpdate(significantEvent, vectorName))

    def connectSearchLogTableEntryTrigger(self, logEntry):
        self.updateSearchLogTableEntryTrigger.connect(lambda: ui.handleSearchLogTableEntryUpdate(logEntry))

    def connectRelationshipTableEntryTrigger(self, logEntry, vectorName):
        self.updateRelationshipTableEntryTrigger.connect(lambda: ui.handleRelationshipTableEntryUpdate(logEntry, vectorName))

    def emitIconTableTrigger(self):
        self.updateIconTableTrigger.emit()

    def emitVectorGraphTrigger(self):
        self.updateVectorGraphTrigger.emit()

    def emitRelationshipTableTrigger(self):
        self.updateRelationshipTableTrigger.emit()

    def emitRelationshipTableEntryTrigger(self):
        self.updateRelationshipTableEntryTrigger.emit()

    def emitVectorTableTrigger(self):
        self.updateVectorTableTrigger.emit()

    def emitVectorTableEntryTrigger(self):
        self.updateVectorTableEntryTrigger.emit()

    def emitSearchLogTableEntryTrigger(self):
        self.updateSearchLogTableEntryTrigger.emit()

class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self, logEntry):
        super(CheckableComboBox, self).__init__()
        self.logEntry = logEntry
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)
        newVectors = list()
        for i in range(self.count()):
            if self.model().item(i, 0).checkState() == QtCore.Qt.Checked:
                newVectors.append(self.associationComboBox.itemText(i))
        ui.clientHandler.vectorManager.handleUpdateToLogEntry(self.logEntry.associatedVectors, newVectors, self.logEntry)

class IconComboBox(QtWidgets.QComboBox):
    def __init__(self, significantEvent):
        super(IconComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))
        self.significantEvent = significantEvent

    def handleItemPressed(self, index):
        newIconName = index.data()
        if newIconName == Icon.DEFAULT:
            self.significantEvent.iconType = Icon.Default
        else:
            self.significantEvent.iconType = newIconName

class VisibilityCheckBox(QtWidgets.QCheckBox):
    def __init__(self, fieldName, vector):
        super(VisibilityCheckBox, self).__init__()
        self.fieldName = fieldName
        self.vector = vector
        self.clicked.connect(self.handleCheck)

    def handleCheck(self):
        self.vector.visibility[self.fieldName] = not self.vector.visibility[self.fieldName]
        ui.updateVectorGraph(self.vector)

class ViewReferenceButton(QtWidgets.QPushButton):
    def __init__(self, logEntry):
        super(ViewReferenceButton, self).__init__()
        self.logEntry = logEntry
        self.clicked.connect(self.handleClick)

    def handleClick(self):
        ui.viewLogEntryClicked(self.logEntry)

class ViewGraphButton(QtWidgets.QPushButton):
    def __init__(self, vector):
        super(ViewGraphButton, self).__init__()
        self.vector = vector
        self.clicked.connect(self.handleClick)

    def handleClick(self):
        ui.viewGraphClicked(self.vector)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PICK = QtWidgets.QMainWindow()
    ui = Ui_PICK()
    ui.setupUi(PICK)
    PICK.show()
    sys.exit(app.exec_())

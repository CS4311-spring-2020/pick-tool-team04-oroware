from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QTableWidgetItem
from GraphWidget import GraphWidget
import sys
import datetime
import xlwt

from LogEntry import LogEntry
from LogEntryPopup import LogEntryPopup
from Globals import logEntryManager
from Globals import vectorManager
from Globals import iconManager
from RelationshipPopup import RelationshipPopup
from SignificantEventPopup import SignificantEventPopup


class Ui_PICK(object):

    def setupMainWindow(self, PICK):
        self.mainWindow = QtWidgets.QWidget(PICK)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainWindow)

    def setupTabWidget(self):
        self.tabWidget = QtWidgets.QTabWidget(self.mainWindow)

    def setupIngestionTab(self):
        self.ingestionTab = QtWidgets.QWidget()
        self.ingestionTabLayout = QtWidgets.QVBoxLayout(self.ingestionTab)

        # Initialize Team Configuration
        self.teamConfiguration = QtWidgets.QFrame(self.ingestionTab)
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
        self.ingestionTabLayout.addWidget(self.teamConfiguration)

        # Intialize Directory Configuration
        self.directoryConfiguration = QtWidgets.QFrame(self.ingestionTab)
        self.directoryConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        self.directoryConfigurationLayout = QtWidgets.QVBoxLayout(self.directoryConfiguration)
        self.directoryConfigurationLabel = QtWidgets.QLabel(self.directoryConfiguration)
        self.directoryConfigurationLayout.addWidget(self.directoryConfigurationLabel)
        self.rootLabel = QtWidgets.QLabel(self.directoryConfiguration)
        self.directoryConfigurationLayout.addWidget(self.rootLabel)
        self.rootTextEdit = QtWidgets.QTextEdit(self.directoryConfiguration)
        self.directoryConfigurationLayout.addWidget(self.rootTextEdit)
        self.redTeamLabel = QtWidgets.QLabel(self.directoryConfiguration)
        self.directoryConfigurationLayout.addWidget(self.redTeamLabel)
        self.redTeamEdit = QtWidgets.QTextEdit(self.directoryConfiguration)
        self.directoryConfigurationLayout.addWidget(self.redTeamEdit)
        self.blueTeamLabel = QtWidgets.QLabel(self.directoryConfiguration)
        self.directoryConfigurationLayout.addWidget(self.blueTeamLabel)
        self.blueTeamEdit = QtWidgets.QTextEdit(self.directoryConfiguration)
        self.directoryConfigurationLayout.addWidget(self.blueTeamEdit)
        self.whiteTeamLabel = QtWidgets.QLabel(self.directoryConfiguration)
        self.directoryConfigurationLayout.addWidget(self.whiteTeamLabel)
        self.whiteTeamEdit = QtWidgets.QTextEdit(self.directoryConfiguration)
        self.directoryConfigurationLayout.addWidget(self.whiteTeamEdit)
        self.ingestionButton = QtWidgets.QPushButton(self.directoryConfiguration)
        self.directoryConfigurationLayout.addWidget(self.ingestionButton)
        self.ingestionTabLayout.addWidget(self.directoryConfiguration)

        # Initialize Event Configuration
        self.eventConfiguration = QtWidgets.QFrame(self.ingestionTab)
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
        self.ingestionTabLayout.addWidget(self.eventConfiguration)
        self.saveEventButton = QtWidgets.QPushButton(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.saveEventButton)

        # Intialize Ingestion Tab
        self.tabWidget.addTab(self.ingestionTab, "")

    def handleVectorComboBoxConfiguration(self, index):
        if self.vectorComboBoxConfiguration.count() > 0:
            global vectorManager
            self.configurationVectorDescriptionTextEdit.setPlainText(vectorManager.vectors[index.data()].vectorDescription)

    def handleVectorComboBoxTable(self, index):
        if self.vectorComboBoxTable.count() > 0:
            global vectorManager
            currentVector = vectorManager.vectors[index.data()]
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
        self.logEntryConfigurationLabel = QtWidgets.QLabel(self.searchLogsTab)
        self.searchLogsLayout.addWidget(self.logEntryConfigurationLabel)
        self.searchLogsTableWidget = QtWidgets.QTableWidget(self.searchLogsTab)
        self.searchLogsTableWidget.setColumnCount(0)
        self.searchLogsTableWidget.setRowCount(0)
        self.searchLogsTableWidget.setMinimumSize(1250, 1750)
        self.searchLogsLayout.addWidget(self.searchLogsTableWidget)
        self.tabWidget.addTab(self.searchLogsTab, "")

    def updateLogTable(self):
        global logEntryManager
        global vectorManager
        logEntries = logEntryManager.logEntriesInTable
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
            logEntryTeamItem = QtWidgets.QTableWidgetItem(logEntryManager.logEntries[rowNum].creator)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Creator"), logEntryTeamItem)
            logEntryArtifactItem = QtWidgets.QTableWidgetItem(logEntryManager.logEntries[rowNum].artifact)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Artifact"), logEntryArtifactItem)
            logEntryEventTypeItem = QtWidgets.QTableWidgetItem(logEntryManager.logEntries[rowNum].eventType)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Event Type"), logEntryEventTypeItem)
            logEntryDateItem = QtWidgets.QTableWidgetItem(logEntryManager.logEntries[rowNum].date)
            self.searchLogsTableWidget.setItem(rowNum, self.colsSearchLogsTable.index("Timestamp"), logEntryDateItem)
            logEntries[rowNum].rowIndexInTable = rowNum
            vectorComboBoxSearchTable = CheckableComboBox()
            counter = 0
            for vector in vectorManager.vectors.values():
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
        global vectorManager
        vectors = vectorManager.vectors
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
            self.vectorConfigurationTableWidget.setItem(rowNum, self.colsVectorConfigurationTable.index("Vector Name"),
                                               vectorNameItem)
            vectorDescriptionItem = QtWidgets.QTableWidgetItem(vector.vectorDescription)
            self.searchLogsTableWidget.setItem(rowNum, self.colsVectorConfigurationTable.index("Vector Description"), vectorDescriptionItem)
            rowNum += 1
        self.searchLogsTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def updateIconConfigurationTable(self):
        global iconManager
        icons = iconManager.icons
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
            if colNum >= 1:
                visibilityCheckboxItem = QtWidgets.QTableWidgetItem()
                visibilityCheckboxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                visibilityCheckboxItem.setCheckState(QtCore.Qt.Unchecked)
                visibilityCheckboxItem.setText("Visible")
                self.vectorTableWidget.setItem(0, colNum, visibilityCheckboxItem)
        rowNum = 1
        while(rowNum < totalRows):
            significantEventIdItem = QtWidgets.QTableWidgetItem(str(significantEvents[rowNum-1].id))
            self.vectorTableWidget.setVerticalHeaderItem(rowNum, significantEventIdItem)
            self.vectorTableWidget.setRowHeight(rowNum, 50)
            significantEventTypeItem = QtWidgets.QTableWidgetItem(significantEvents[rowNum-1].logEntry.eventType)
            viewEntryButton = QtWidgets.QPushButton()
            viewEntryButton.setText("View Log Entry")
            self.vectorTableWidget.setCellWidget(rowNum, self.colsVectorTable.index("Reference"),
                                                     viewEntryButton)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Event Type"), significantEventTypeItem)
            significantEventIconTypeItem = QtWidgets.QTableWidgetItem(significantEvents[rowNum-1].iconType)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Icon Type"), significantEventIconTypeItem)
            significantEventNameItem = QtWidgets.QTableWidgetItem(significantEvents[rowNum-1].name)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Node Name"), significantEventNameItem)
            significantEventDateItem = QtWidgets.QTableWidgetItem(significantEvents[rowNum-1].logEntry.date)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Node Timestamp"), significantEventDateItem)
            significantEventCreatorItem = QtWidgets.QTableWidgetItem(significantEvents[rowNum-1].logEntry.creator)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Event Creator"), significantEventCreatorItem)
            significantEventDescriptionItem = QtWidgets.QTableWidgetItem(significantEvents[rowNum-1].description)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Node Description"), significantEventDescriptionItem)
            significantEventArtifactItem = QtWidgets.QTableWidgetItem(significantEvents[rowNum-1].logEntry.artifact)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Artifact"), significantEventArtifactItem)
            significantEvents[rowNum-1].rowIndexInTable = rowNum
            rowNum += 1
        self.vectorTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # self.vectorTableWidget.doubleClicked.connect(self.vectorTableDoubleClicked)

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
            self.relationshipTableWidget.setItem(rowNum, len(self.colsRelationshipTable) - 3, relationshipSourceItem)
            relationshipDestItem = QtWidgets.QTableWidgetItem(str(relationships[rowNum].destSignificantEventId))
            self.relationshipTableWidget.setItem(rowNum, len(self.colsRelationshipTable) - 2, relationshipDestItem)
            relationshipDescriptionItem = QtWidgets.QTableWidgetItem(relationships[rowNum].description)
            self.relationshipTableWidget.setItem(rowNum, len(self.colsRelationshipTable) - 1, relationshipDescriptionItem)
            relationships[rowNum].rowIndexInTable = rowNum
        self.relationshipTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # self.relationshipTableWidget.doubleClicked.connect(self.relationshipTableDoubleClicked)

    def updateVectorGraph(self, vector):
        self.vectorGraphWidget.initializeVector(vector)
        self.vectorGraphWidget.draw()

    def searchTableDoubleClicked(self):
        global logEntryManager
        logEntryId = self.searchLogsTableWidget.verticalHeaderItem(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        logEntry = logEntryManager.logEntries[int(logEntryId)]
        logEntryDescriptionWidget = self.searchLogsTableWidget.item(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Content"))
        associatedVectorsWidget = self.searchLogsTableWidget.cellWidget(self.searchLogsTableWidget.selectionModel().selectedIndexes()[0].row(), self.colsSearchLogsTable.index("Vectors"))
        self.editPopup = LogEntryPopup(logEntry, logEntryDescriptionWidget, associatedVectorsWidget)
        self.editPopup.setGeometry(100, 200, 100, 100)
        self.editPopup.show()

    def vectorTableDoubleClicked(self):
        global vectorManager
        trigger = TriggerHelper()
        significantEventId = self.vectorTableWidget.verticalHeaderItem(self.vectorTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        vectorName = self.vectorComboBoxTable.currentText()
        vector = vectorManager.vectors[vectorName]
        significantEventToEdit = vector.significantEvents[int(significantEventId)]
        self.editVectorPopup = SignificantEventPopup(vector, significantEventToEdit, trigger)
        self.editVectorPopup.setGeometry(100, 200, 100, 100)
        self.editVectorPopup.show()

    def relationshipTableDoubleClicked(self):
        global vectorManager
        trigger = TriggerHelper()
        relationshipId = self.relationshipTableWidget.verticalHeaderItem(self.relationshipTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        vectorName = self.vectorComboBoxTable.currentText()
        vector = vectorManager.vectors[vectorName]
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
        self.filterGraphLayout.addWidget(self.zoomInButtonGraph)
        self.zoomOutButtonGraph = QtWidgets.QPushButton(self.graphFrame)
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
        self.addNodeTableButton = QtWidgets.QPushButton(self.vectorFrame)
        self.addNodeTableButton.clicked.connect(self.handleAddNode)
        self.editVectorTableLayout.addWidget(self.addNodeTableButton)
        self.exportTableButton = QtWidgets.QPushButton(self.vectorFrame)
        self.exportTableButton.clicked.connect(self.handleExport)
        self.editVectorTableLayout.addWidget(self.exportTableButton)
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
        self.tabWidget.currentChanged.connect(self.onTabChange)

    def setupIconConfigurationTab(self):
        self.iconConfigurationTab = QtWidgets.QWidget()
        self.iconConfigurationLayout = QtWidgets.QVBoxLayout(self.iconConfigurationTab)
        self.iconConfigurationLabel = QtWidgets.QLabel(self.iconConfigurationTab)
        self.iconConfigurationLayout.addWidget(self.iconConfigurationLabel)
        self.addIconButton = QtWidgets.QPushButton(self.iconConfigurationTab)
        self.iconConfigurationLayout.addWidget(self.addIconButton)
        self.iconConfigurationTableWidget = QtWidgets.QTableWidget(self.iconConfigurationTab)
        self.iconConfigurationTableWidget.setColumnCount(0)
        self.iconConfigurationTableWidget.setRowCount(0)
        self.iconConfigurationTableWidget.setMinimumSize(1250, 1750)
        self.iconConfigurationLayout.addWidget(self.iconConfigurationTableWidget)
        self.tabWidget.addTab(self.iconConfigurationTab, "")

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
            self.searchLogsTableWidget.setItem(logEntry.rowIndexInTable, len(self.colsSearchLogsTable) - 1,
                                                   logEntryDescriptionItem)

    def handleRelationshipTableEntryUpdate(self, relationship, vectorName):
        if relationship.rowIndexInTable != -1 and self.vectorComboBoxTable.count() > 0 and self.vectorComboBoxTable.currentText() == vectorName:
            relationshipDescriptionItem = QtWidgets.QTableWidgetItem(relationship.description)
            self.relationshipTableWidget.setItem(relationship.rowIndexInTable, len(self.colsRelationshipTable) - 1,
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
            global vectorManager
            global logEntryManager
            vector = vectorManager.vectors[vectorName]
            logEntry = LogEntry()
            logEntry.creator = logEntry.WHITE_TEAM
            logEntry.id = logEntryManager.nextAvailableId
            logEntryManager.nextAvailableId += 1
            logEntry.date = (datetime.datetime.today()).strftime("%m/%d/%Y %I:%M %p").lstrip("0")
            logEntry.associatedVectors.append(self.vectorComboBoxTable.currentText())
            vector.addSignificantEventFromLogEntry(logEntry)
            self.updateVectorTable(vector)
            self.updateVectorGraph(vector)

    def onTabChange(self):
        if self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.editVectorTab) and self.vectorComboBoxTable.count() > 0:
            vectorName = self.vectorComboBoxTable.currentText()
            global vectorManager
            vector = vectorManager.vectors[vectorName]
            self.updateVectorTable(vector)
            self.updateRelationshipTable(vector)
            self.updateVectorGraph(vector)

    def handleRelationshipTableTrigger(self):
        if self.vectorComboBoxTable.count() > 0:
            vectorName = self.vectorComboBoxTable.currentText()
            global vectorManager
            vector = vectorManager.vectors[vectorName]
            self.updateRelationshipTable(vector)

    def handleVectorGraphTrigger(self):
        if self.vectorComboBoxTable.count() > 0:
            vectorName = self.vectorComboBoxTable.currentText()
            global vectorManager
            vector = vectorManager.vectors[vectorName]
            self.updateVectorGraph(vector)

    def updateVectorComboBoxes(self):
        vectorNames = (vectorManager.vectors.keys())
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

        # Table column names
        self.colsSearchLogsTable = ["Timestamp", "Content", "Artifact", "Creator", "Event Type", "Vectors"]
        self.colsVectorConfigurationTable = ["Vector Name", "Vector Description"]
        self.colsIconConfigurationTable = ["Icon Name", "Icon Source", "Icon Preview"]
        self.colsVectorTable = ["Node Name", "Node Timestamp", "Node Description", "Reference", "Event Creator", "Event Type", "Icon Type", "Artifact"]
        self.colsRelationshipTable = ["Parent", "Child", "Description"]

        # Vector list
        self.vectors = list()
        # Initialization of vector list
        global vectorManager
        global logEntryManager
        logEntryManager.vectorManager = vectorManager
        self.vectors = list(vectorManager.vectors.values())

        self.setupMainWindow(PICK)
        self.setupTabWidget()
        self.setupIngestionTab()
        self.setupSearchLogsTab()
        self.setupVectorConfigurationTab()
        self.setupIconConfigurationTab()
        logEntryManager.searchLogEntryTableWidget = self.searchLogsTableWidget
        logEntryManager.colNamesInSearchLogsTable = self.colsSearchLogsTable
        self.updateLogTable()
        self.updateVectorConfigurationTable()
        self.updateIconConfigurationTable()
        self.setupEditVectorTab()
        self.updateVectorComboBoxes()

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
        self.teamConfigurationLabel.setText("TEAM CONFIGURATION")
        self.teamConfigurationLabel.setText("TEAM CONFIGURATION")
        self.eventConfigurationLabel.setText("EVENT CONFIGURATION")
        self.leadCheckBox.setText("Lead")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ingestionTab), "Ingestion")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.vectorConfigurationTab), "Vector Configuration")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.iconConfigurationTab), "Icon Configuration")
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
        self.toSearchLabel.setText("End Timestamp:")
        self.redTeamLabel.setText("Red Team Folder: ")
        self.searchButton.setText("Apply Filter")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.searchLogsTab), "Search Logs")
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
        self.logEntryConfigurationLabel.setText("LOG ENTRY CONFIGURATION")
        self.saveEventButton.setText("Save Event")
        self.ingestionButton.setText("Start Data Ingestion")
        self.eventDescriptionLabel.setText("Event description: ")
        self.addNodeTableButton.setText("Add Node")
        self.establishedConnectionsLabel.setText("No. of established connections to the lead’s IP address: " + str(self.establishedConnections))
        self.numConnectionsLabel.setText("No. of connections to the lead’s IP address: " + str(self.numConnections))
        self.exportTableButton.setText("Export Vector")
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

    def connectRelationshipTableTrigger(self):
        self.updateRelationshipTableTrigger.connect(ui.handleRelationshipTableTrigger)

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
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PICK = QtWidgets.QMainWindow()
    ui = Ui_PICK()
    ui.setupUi(PICK)
    PICK.show()
    sys.exit(app.exec_())

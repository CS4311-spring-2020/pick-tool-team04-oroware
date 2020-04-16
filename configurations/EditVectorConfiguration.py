import datetime

import xlwt
import csv
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QShortcut

from ExportPopup import ExportPopup
from GraphWidget import GraphWidget
from Icon import Icon
from LogEntry import LogEntry
from LogEntryViewPopup import LogEntryViewPopup
from RelationshipPopup import RelationshipPopup
from SignificantEventPopup import SignificantEventPopup


class EditVectorConfiguration(QWidget):
    def __init__(self, clientHandler, triggerHelper):
        super(EditVectorConfiguration, self).__init__()
        self.clientHandler = clientHandler
        self.triggerHelper = triggerHelper
        self.colsIconConfigurationTable = ["Icon Name", "Icon Source", "Icon Preview"]
        self.colsVectorTable = ["Visibility", "Name", "Timestamp", "Description", "Reference", "Event Creator", "Event Type", "Icon Type", "Artifact"]
        self.colsRelationshipTable = ["Parent", "Child", "Label"]
        self.editVectorLayout = QtWidgets.QHBoxLayout(self)
        self.leftEditVectorWidget = QtWidgets.QWidget(self)
        self.leftEditVectorLayout = QtWidgets.QVBoxLayout(self.leftEditVectorWidget)
        self.vectorGraphWidget = GraphWidget(self.leftEditVectorWidget, triggerHelper)
        self.leftEditVectorLayout.addWidget(self.vectorGraphWidget)
        self.editVectorLayout.addWidget(self.leftEditVectorWidget, 1)

        self.rightEditVectorWidget = QtWidgets.QWidget(self)
        self.rightEditVectorLayout = QtWidgets.QVBoxLayout(self.rightEditVectorWidget)
        self.vectorTableLabel = QtWidgets.QLabel(self.rightEditVectorWidget)
        self.rightEditVectorLayout.addWidget(self.vectorTableLabel)
        self.vectorComboBoxTable = QtWidgets.QComboBox(self.rightEditVectorWidget)
        self.vectorComboBoxTable.setFont(QtGui.QFont('SansSerif', 7))
        self.vectorComboBoxTable.view().pressed.connect(self.handleVectorComboBoxTable)
        self.rightEditVectorLayout.addWidget(self.vectorComboBoxTable)
        self.vectorDescriptionLabel = QtWidgets.QLabel(self.rightEditVectorWidget)
        self.vectorDescriptionLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.rightEditVectorLayout.addWidget(self.vectorDescriptionLabel)
        self.exportTableButton = QtWidgets.QPushButton(self.rightEditVectorWidget)
        self.exportTableButton.clicked.connect(self.handleExport)
        self.rightEditVectorLayout.addWidget(self.exportTableButton)
        self.addNodeTableButton = QtWidgets.QPushButton(self.rightEditVectorWidget)
        self.addNodeTableButton.clicked.connect(self.handleAddNode)
        self.rightEditVectorLayout.addWidget(self.addNodeTableButton)
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
        self.editVectorLayout.addWidget(self.rightEditVectorWidget, 1)

        self.zoomInShortcut = QShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Up), self)
        self.zoomInShortcut.activated.connect(self.handleZoomInShortcut)
        self.zoomOutShortcut = QShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Down), self)
        self.zoomOutShortcut.activated.connect(self.handleZoomOutShortcut)
        self.intializeText()

    @pyqtSlot()
    def handleZoomInShortcut(self):
       self.vectorGraphWidget.maximize()

    @pyqtSlot()
    def handleZoomOutShortcut(self):
        self.vectorGraphWidget.minimize()

    def clearVectorTable(self):
        self.vectorTableWidget.setColumnCount(len(self.colsVectorTable))
        self.vectorTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.vectorTableWidget.setRowCount(0)
        header = self.vectorTableWidget.horizontalHeader()
        for colNum in range(len(self.colsVectorTable)):
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsVectorTable[colNum])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorTableWidget.setHorizontalHeaderItem(colNum, headerItem)

    def clearRelationshipTable(self):
        self.relationshipTableWidget.setColumnCount(len(self.colsRelationshipTable))
        self.relationshipTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.relationshipTableWidget.setRowCount(0)
        header = self.relationshipTableWidget.horizontalHeader()
        for colNum in range(len(self.colsRelationshipTable)):
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsRelationshipTable[colNum])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.relationshipTableWidget.setHorizontalHeaderItem(colNum, headerItem)

    def updateVectorTable(self, vector):
        self.clientHandler.vectorManager.storeVectors()
        if self.clientHandler.isLead:
            self.clientHandler.updateVector(vector)
        significantEvents = list(vector.significantEvents.values())
        totalRows = len(significantEvents) + 1
        self.vectorTableWidget.setColumnCount(len(self.colsVectorTable))
        self.vectorTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.vectorTableWidget.setRowCount(totalRows)
        header = self.vectorTableWidget.horizontalHeader()
        for colNum in range(len(self.colsVectorTable)):
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsVectorTable[colNum])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorTableWidget.setHorizontalHeaderItem(colNum, headerItem)
            if colNum == self.colsVectorTable.index("Visibility"):
                nodeVisibilityCheckbox = NodeVisibilityCheckBox(self.updateVectorGraph, self.updateVectorTable, None, vector, True)
                nodeVisibilityCheckbox.setFont(QtGui.QFont('SansSerif', 7))
                nodeVisibilityCheckbox.setCheckState(QtCore.Qt.Checked if vector.allVisible else QtCore.Qt.Unchecked)
                nodeVisibilityCheckbox.setText("All")
                self.vectorTableWidget.setCellWidget(0, colNum, nodeVisibilityCheckbox)
                continue
            if colNum != self.colsVectorTable.index("Icon Type") and colNum != self.colsVectorTable.index("Reference"):
                visibilityCheckbox = VisibilityCheckBox(self.colsVectorTable[colNum], self.updateVectorGraph, vector)
                visibilityCheckbox.setFont(QtGui.QFont('SansSerif', 7))
                visibilityCheckbox.setCheckState(QtCore.Qt.Checked if vector.visibility[self.colsVectorTable[colNum]] else QtCore.Qt.Unchecked)
                visibilityCheckbox.setText("Visible")
                self.vectorTableWidget.setCellWidget(0, colNum, visibilityCheckbox)
        placerHeaderItem = QtWidgets.QTableWidgetItem("")
        placerHeaderItem.setFont(QtGui.QFont('SansSerif', 7))
        self.vectorTableWidget.setVerticalHeaderItem(0, placerHeaderItem)
        rowNum = 1
        while(rowNum < totalRows):
            significantEvent = significantEvents[rowNum-1]
            significantEventIdItem = QtWidgets.QTableWidgetItem(str(significantEvent.id))
            significantEventIdItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorTableWidget.setVerticalHeaderItem(rowNum, significantEventIdItem)
            self.vectorTableWidget.setRowHeight(rowNum, 50)
            significantEventTypeItem = QtWidgets.QTableWidgetItem(significantEvent.logEntry.eventType)
            significantEventTypeItem.setFont(QtGui.QFont('SansSerif', 7))
            logEntry = significantEvent.logEntry
            viewEntryButton = ViewReferenceButton(logEntry)
            viewEntryButton.setFont(QtGui.QFont('SansSerif', 7))
            viewEntryButton.setText("View Log Entry")
            self.vectorTableWidget.setCellWidget(rowNum, self.colsVectorTable.index("Reference"),
                                                     viewEntryButton)
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Event Type"), significantEventTypeItem)
            iconComboBox = IconComboBox(significantEvent, self.clientHandler, self.updateVectorGraph, vector.vectorName)
            iconComboBox.setFont(QtGui.QFont('SansSerif', 7))
            if significantEvent.icon:
                iconComboBox.addItem(significantEvent.icon.name)
            iconComboBox.addItem(Icon.DEFAULT)
            for iconName, icon in self.clientHandler.iconManager.icons.items():
                if significantEvent.icon:
                    if iconName != significantEvent.icon.name:
                        iconComboBox.addItem(iconName)
                else:
                    iconComboBox.addItem(iconName)
            self.vectorTableWidget.setCellWidget(rowNum, self.colsVectorTable.index("Icon Type"), iconComboBox)
            significantEventNameItem = QtWidgets.QTableWidgetItem(significantEvent.name)
            significantEventNameItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Name"), significantEventNameItem)
            significantEventDateItem = QtWidgets.QTableWidgetItem(significantEvent.logEntry.date)
            significantEventDateItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Timestamp"), significantEventDateItem)
            significantEventCreatorItem = QtWidgets.QTableWidgetItem(significantEvent.logEntry.creator)
            significantEventCreatorItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Event Creator"), significantEventCreatorItem)
            significantEventDescriptionItem = QtWidgets.QTableWidgetItem(significantEvent.description)
            significantEventDescriptionItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Description"), significantEventDescriptionItem)
            significantEventArtifactItem = QtWidgets.QTableWidgetItem(significantEvent.logEntry.artifact)
            significantEventArtifactItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorTableWidget.setItem(rowNum, self.colsVectorTable.index("Artifact"), significantEventArtifactItem)
            nodeVisibilityCheckbox = NodeVisibilityCheckBox(self.updateVectorGraph, self.updateVectorTable, significantEvent, vector, False)
            nodeVisibilityCheckbox.setFont(QtGui.QFont('SansSerif', 7))
            nodeVisibilityCheckbox.setCheckState(QtCore.Qt.Checked if significantEvent.visible else QtCore.Qt.Unchecked)
            self.vectorTableWidget.setCellWidget(rowNum, self.colsVectorTable.index("Visibility"), nodeVisibilityCheckbox)
            significantEvent.rowIndexInTable = rowNum
            rowNum += 1
        self.vectorTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.vectorTableWidget.doubleClicked.connect(self.vectorTableDoubleClicked)

    def handleRelationshipTableEntryUpdate(self, relationship, vectorName):
        if relationship.rowIndexInTable != -1 and self.vectorComboBoxTable.count() > 0 and self.vectorComboBoxTable.currentText() == vectorName:
            relationshipDescriptionItem = QtWidgets.QTableWidgetItem(relationship.description)
            relationshipDescriptionItem.setFont(QtGui.QFont('SansSerif', 7))
            self.relationshipTableWidget.setItem(relationship.rowIndexInTable, self.colsRelationshipTable.index("Label"),
                                                   relationshipDescriptionItem)

    def onTabChange(self):
        if self.vectorComboBoxTable.count() > 0:
            self.leftEditVectorLayout.removeWidget(self.vectorGraphWidget)
            self.triggerHelper.connectRelationshipTableTrigger()
            self.vectorGraphWidget = GraphWidget(self.leftEditVectorWidget, self.triggerHelper, self.clientHandler)
            self.leftEditVectorLayout.addWidget(self.vectorGraphWidget)
            vectorName = self.vectorComboBoxTable.currentText()
            vector = self.clientHandler.vectorManager.vectors[vectorName]
            self.updateVectorTable(vector)
            self.updateRelationshipTable(vector)
            self.updateVectorGraph(vector)
        else:
            self.leftEditVectorLayout.removeWidget(self.vectorGraphWidget)
            self.triggerHelper.connectRelationshipTableTrigger()
            self.vectorGraphWidget = GraphWidget(self.leftEditVectorWidget, self.triggerHelper, self.clientHandler)
            self.leftEditVectorLayout.addWidget(self.vectorGraphWidget)
            self.clearVectorTable()
            self.clearRelationshipTable()

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

    def handleVectorTableEntryUpdate(self, significantEvent, vectorName):
        if significantEvent.rowIndexInTable != -1 and self.vectorComboBoxTable.count() > 0 and self.vectorComboBoxTable.currentText() == vectorName:
            significantEventDescriptionItem = QtWidgets.QTableWidgetItem(significantEvent.logEntry.description)
            significantEventDescriptionItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorTableWidget.setItem(significantEvent.rowIndexInTable, len(self.colsVectorTable) - 1,
                                                   significantEventDescriptionItem)

    def updateRelationshipTable(self, vector):
        self.clientHandler.vectorManager.storeVectors()
        if self.clientHandler.isLead:
            self.clientHandler.updateVector(vector)
        relationships = list(vector.relationships.values())
        totalRows = len(relationships)
        self.relationshipTableWidget.setColumnCount(len(self.colsRelationshipTable))
        self.relationshipTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.relationshipTableWidget.setRowCount(totalRows)
        header = self.relationshipTableWidget.horizontalHeader()
        for colNum in range(len(self.colsRelationshipTable)):
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsRelationshipTable[colNum])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.relationshipTableWidget.setHorizontalHeaderItem(colNum, headerItem)
        for rowNum in range(totalRows):
            self.relationshipTableWidget.setRowHeight(rowNum, 50)
            relationshipIdItem = QtWidgets.QTableWidgetItem(str(relationships[rowNum].id))
            relationshipIdItem.setFont(QtGui.QFont('SansSerif', 7))
            self.relationshipTableWidget.setVerticalHeaderItem(rowNum, relationshipIdItem)
            relationshipSourceItem = QtWidgets.QTableWidgetItem(str(relationships[rowNum].sourceSignificantEventId))
            relationshipSourceItem.setFont(QtGui.QFont('SansSerif', 7))
            self.relationshipTableWidget.setItem(rowNum, self.colsRelationshipTable.index("Parent"), relationshipSourceItem)
            relationshipDestItem = QtWidgets.QTableWidgetItem(str(relationships[rowNum].destSignificantEventId))
            relationshipDestItem.setFont(QtGui.QFont('SansSerif', 7))
            self.relationshipTableWidget.setItem(rowNum, self.colsRelationshipTable.index("Child"), relationshipDestItem)
            relationshipDescriptionItem = QtWidgets.QTableWidgetItem(relationships[rowNum].description)
            relationshipDescriptionItem.setFont(QtGui.QFont('SansSerif', 7))
            self.relationshipTableWidget.setItem(rowNum, self.colsRelationshipTable.index("Label"), relationshipDescriptionItem)
            relationships[rowNum].rowIndexInTable = rowNum
        self.relationshipTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.relationshipTableWidget.doubleClicked.connect(self.relationshipTableDoubleClicked)

    def handleExport(self):
        if self.vectorComboBoxTable.count() > 0:
            self.exportPopup = ExportPopup(self.vectorComboBoxTable.currentText(), self.vectorTableWidget, self.relationshipTableWidget, self.vectorGraphWidget.figure)
            self.exportPopup.setGeometry(100, 200, 200, 200)
            self.exportPopup.show()

    def updateComboBox(self):
        vectorNames = (self.clientHandler.vectorManager.vectors.keys())
        self.vectorComboBoxTable.clear()
        for vectorName in vectorNames:
            self.vectorComboBoxTable.addItem(vectorName)

    def handleVectorComboBoxTable(self, index):
        if self.vectorComboBoxTable.count() > 0:
            currentVector = self.clientHandler.vectorManager.vectors[index.data()]
            self.vectorDescriptionLabel.setText("Vector Description: " + currentVector.vectorDescription)
            self.updateVectorTable(currentVector)
            self.updateRelationshipTable(currentVector)
            self.updateVectorGraph(currentVector)

    def intializeText(self):
        self.addNodeTableButton.setText("Add Node")
        self.addNodeTableButton.setFont(QtGui.QFont('SansSerif', 7))
        self.nodeTableLabel.setText("Nodes:")
        self.nodeTableLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.relationshipTableLabel.setText("Relationships:")
        self.relationshipTableLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.vectorTableLabel.setText("Vector:")
        self.vectorTableLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.exportTableButton.setText("Export Vector")
        self.exportTableButton.setFont(QtGui.QFont('SansSerif', 7))

    def updateVectorGraph(self, vector):
        self.clientHandler.vectorManager.storeVectors()
        if self.clientHandler.isLead:
            self.clientHandler.updateVector(vector)
        self.vectorGraphWidget.initializeVector(vector)
        self.vectorGraphWidget.draw()

    def handleAddNode(self):
        if self.vectorComboBoxTable.count() > 0:
            vectorName = self.vectorComboBoxTable.currentText()
            vector = self.clientHandler.vectorManager.vectors[vectorName]
            logEntry = LogEntry()
            logEntry.creator = logEntry.WHITE_TEAM
            logEntry.eventType = logEntry.WHITE_TEAM
            logEntry.id = "-1"
            logEntry.date = (datetime.datetime.today()).strftime("%m/%d/%Y %I:%M %p").lstrip("0")
            logEntry.associatedVectors.append(self.vectorComboBoxTable.currentText())
            vector.addSignificantEventFromLogEntry(logEntry)
            self.updateVectorTable(vector)
            self.updateVectorGraph(vector)
            self.updateVectorGraph(vector)

    def vectorTableDoubleClicked(self):
        significantEventId = self.vectorTableWidget.verticalHeaderItem(self.vectorTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        vectorName = self.vectorComboBoxTable.currentText()
        vector = self.clientHandler.vectorManager.vectors[vectorName]
        significantEventToEdit = vector.significantEvents[int(significantEventId)]
        self.editEventPopup = SignificantEventPopup(vector, significantEventToEdit, self.triggerHelper, self.clientHandler.isLead, self.clientHandler.logEntryManager)
        self.editEventPopup.setGeometry(100, 200, 200, 200)
        self.editEventPopup.show()

    def relationshipTableDoubleClicked(self):
        relationshipId = self.relationshipTableWidget.verticalHeaderItem(self.relationshipTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        vectorName = self.vectorComboBoxTable.currentText()
        vector = self.clientHandler.vectorManager.vectors[vectorName]
        relationshipToEdit = vector.relationships[int(relationshipId)]
        self.editRelationshipPopup = RelationshipPopup(vector, relationshipToEdit, self.triggerHelper)
        self.editRelationshipPopup.setGeometry(100, 200, 100, 100)
        self.editRelationshipPopup.show()

class ViewReferenceButton(QtWidgets.QPushButton):
    def __init__(self, logEntry):
        super(ViewReferenceButton, self).__init__()
        self.logEntry = logEntry
        self.clicked.connect(self.handleClick)

    def handleClick(self):
        self.viewLogEntryClicked(self.logEntry)

    def viewLogEntryClicked(self, logEntry):
        self.viewPopup = LogEntryViewPopup(logEntry)
        self.viewPopup.setGeometry(100, 200, 200, 200)
        self.viewPopup.show()

class VisibilityCheckBox(QtWidgets.QCheckBox):
    def __init__(self, fieldName, updateVectorGraph, vector):
        super(VisibilityCheckBox, self).__init__()
        self.fieldName = fieldName
        self.vector = vector
        self.clicked.connect(self.handleCheck)
        self.updateVectorGraph = updateVectorGraph

    def handleCheck(self):
        self.vector.visibility[self.fieldName] = not self.vector.visibility[self.fieldName]
        self.updateVectorGraph(self.vector)

class NodeVisibilityCheckBox(QtWidgets.QCheckBox):
    def __init__(self, updateVectorGraph, updateVectorTable, significantEvent, vector, allSelected):
        super(NodeVisibilityCheckBox, self).__init__()
        self.significantEvent = significantEvent
        self.allSelected = allSelected
        self.vector = vector
        self.clicked.connect(self.handleCheck)
        self.updateVectorGraph = updateVectorGraph
        self.updateVectorTable = updateVectorTable

    def handleCheck(self):
        if self.allSelected:
            if self.isChecked():
                self.vector.allVisible = True
                for significantEvent in list(self.vector.significantEvents.values()):
                    significantEvent.visible = True
            else:
                self.vector.allVisible = False
                for significantEvent in list(self.vector.significantEvents.values()):
                    significantEvent.visible = False
            self.updateVectorGraph(self.vector)
            self.updateVectorTable(self.vector)
        else:
            self.significantEvent.visible = not self.significantEvent.visible
            self.updateVectorGraph(self.vector)

class IconComboBox(QtWidgets.QComboBox):
    def __init__(self, significantEvent, clientHandler, updateVectorGraph, vectorName):
        super(IconComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))
        self.significantEvent = significantEvent
        self.clientHandler = clientHandler
        self.vectorName = vectorName
        self.updateVectorGraph = updateVectorGraph

    def handleItemPressed(self, index):
        newIconName = index.data()
        if newIconName == Icon.DEFAULT:
            self.significantEvent.iconType = Icon.DEFAULT
            self.significantEvent.icon = None
            self.updateVectorGraph(self.clientHandler.vectorManager.vectors[self.vectorName])
        else:
            self.significantEvent.iconType = Icon.CUSTOM
            self.significantEvent.icon = self.clientHandler.iconManager.icons[newIconName]
            self.updateVectorGraph(self.clientHandler.vectorManager.vectors[self.vectorName])
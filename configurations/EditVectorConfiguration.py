import datetime

import xlwt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

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
        self.colsVectorTable = ["Node Name", "Node Timestamp", "Node Description", "Reference", "Event Creator", "Event Type", "Icon Type", "Artifact"]
        self.colsRelationshipTable = ["Parent", "Child", "Label"]
        self.editVectorLayout = QtWidgets.QHBoxLayout(self)
        self.leftEditVectorWidget = QtWidgets.QWidget(self)
        self.leftEditVectorLayout = QtWidgets.QVBoxLayout(self.leftEditVectorWidget)
        self.graphWidget = QtWidgets.QWidget(self.leftEditVectorWidget)
        self.graphLayout = QtWidgets.QVBoxLayout(self.graphWidget)
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
        self.rightEditVectorWidget = QtWidgets.QWidget(self)
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
        self.intializeText()

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
                visibilityCheckbox = VisibilityCheckBox(self.colsVectorTable[colNum], self.updateVectorGraph, vector)
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
            iconComboBox = IconComboBox(significantEvent, self.clientHandler, self.updateVectorGraph, vector.vectorName)
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

    def handleRelationshipTableEntryUpdate(self, relationship, vectorName):
        if relationship.rowIndexInTable != -1 and self.vectorComboBoxTable.count() > 0 and self.vectorComboBoxTable.currentText() == vectorName:
            relationshipDescriptionItem = QtWidgets.QTableWidgetItem(relationship.description)
            self.relationshipTableWidget.setItem(relationship.rowIndexInTable, self.colsRelationshipTable.index("Label"),
                                                   relationshipDescriptionItem)

    def onTabChange(self):
        if self.vectorComboBoxTable.count() > 0:
            self.graphLayout.removeWidget(self.vectorGraphWidget)
            self.triggerHelper.connectRelationshipTableTrigger()
            self.vectorGraphWidget = GraphWidget(self.graphWidget, self.triggerHelper)
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

    def handleSearchLogTableEntryUpdate(self, logEntry):
        if logEntry.rowIndexInTable != -1:
            logEntryDescriptionItem = QtWidgets.QTableWidgetItem(logEntry.description)
            self.searchLogsTableWidget.setItem(logEntry.rowIndexInTable, self.colsSearchLogsTable.index("Content"),
                                                   logEntryDescriptionItem)

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
            self.vectorTableWidget.setItem(significantEvent.rowIndexInTable, len(self.colsVectorTable) - 1,
                                                   significantEventDescriptionItem)

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

    def handleExport(self):
        if self.vectorComboBoxTable.count() > 0:
            self.vectorGraphWidget.export()
            self.exportVectorTable(self.vectorComboBoxTable.currentText())
            self.exportRelationshipTable(self.vectorComboBoxTable.currentText())

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

    def intializeText(self):
        self.addNodeTableButton.setText("Add Node")
        self.nodeTableLabel.setText("Nodes:")
        self.relationshipTableLabel.setText("Relationships:")
        self.zoomInButtonGraph.setText("Zoom In")
        self.zoomOutButtonGraph.setText("Zoom Out")
        self.vectorTableLabel.setText("Vector:")
        self.exportTableButton.setText("Export Vector")
        self.addNodeGraphButton.setText("Add Node")

    def updateVectorGraph(self, vector):
        self.vectorGraphWidget.initializeVector(vector)
        self.vectorGraphWidget.draw()

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

    def vectorTableDoubleClicked(self):
        significantEventId = self.vectorTableWidget.verticalHeaderItem(self.vectorTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        vectorName = self.vectorComboBoxTable.currentText()
        vector = self.clientHandler.vectorManager.vectors[vectorName]
        significantEventToEdit = vector.significantEvents[int(significantEventId)]
        self.editEventPopup = SignificantEventPopup(vector, significantEventToEdit, self.trigger)
        self.editEventPopup.setGeometry(100, 200, 200, 200)
        self.editEventPopup.show()

    def relationshipTableDoubleClicked(self):
        relationshipId = self.relationshipTableWidget.verticalHeaderItem(self.relationshipTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        vectorName = self.vectorComboBoxTable.currentText()
        vector = self.clientHandler.vectorManager.vectors[vectorName]
        relationshipToEdit = vector.relationships[int(relationshipId)]
        self.editRelationshipPopup = RelationshipPopup(vector, relationshipToEdit, self.trigger)
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
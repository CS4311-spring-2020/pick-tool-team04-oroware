from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout
from copy import deepcopy

from GraphWidget import GraphWidget
from VectorManager import VectorManager


class VectorDbConfiguration(QWidget):
    def __init__(self, clientHandler, triggerHelper):
        super(VectorDbConfiguration, self).__init__()
        self.clientHandler = clientHandler
        self.triggerHelper = triggerHelper
        self.colsPullTable = ["Vector Name", "Vector Description", "Vector Graph"]
        self.colsPushTable = ["Vector Name", "Vector Description", "Change Summary", "Vector Graph"]
        self.colsApproveTable = ["Source IP", "Request Timestamp", "Vector Name", "Vector Description", "Graph", "Approve"]
        self.pushedVectorManager = VectorManager()
        self.pushedVectorManager.filename = "pushedVectors.pkl"
        self.pushedVectorManager.retrieveVectors()
        self.pulledVectorManager = VectorManager()
        self.pulledVectorManager.filename = "pulledVectors.pkl"
        self.pulledVectorManager.retrieveVectors()
        self.pendingVectors = dict()
        self.vectorDbLayout = QtWidgets.QVBoxLayout(self)
        self.initializeConfiguration()

    def initializeConfiguration(self):
        for i in reversed(range(self.vectorDbLayout.count())):
            self.vectorDbLayout.removeWidget(self.vectorDbLayout.itemAt(i).widget())
        self.vectorDbLabel = QtWidgets.QLabel(self)
        self.vectorDbLayout.addWidget(self.vectorDbLabel)
        if self.clientHandler.isLead:
            self.approvalLabel = QtWidgets.QLabel(self)
            self.vectorDbLayout.addWidget(self.approvalLabel)
            self.approvalTableWidget = QtWidgets.QTableWidget(self)
            self.approvalTableWidget.setColumnCount(0)
            self.approvalTableWidget.setRowCount(0)
            self.vectorDbLayout.addWidget(self.approvalTableWidget)
            self.updateApproveTable(self.pendingVectors)
        else:
            self.pullTableLabel = QtWidgets.QLabel(self)
            self.vectorDbLayout.addWidget(self.pullTableLabel)
            self.pullTableWidget = QtWidgets.QTableWidget(self)
            self.pullTableWidget.setColumnCount(0)
            self.pullTableWidget.setRowCount(0)
            self.vectorDbLayout.addWidget(self.pullTableWidget)
            self.pullButton = QtWidgets.QPushButton(self)
            self.pullButton.clicked.connect(self.handlePull)
            self.vectorDbLayout.addWidget(self.pullButton)
            self.pushTableLabel = QtWidgets.QLabel(self)
            self.vectorDbLayout.addWidget(self.pushTableLabel)
            self.pushTableWidget = QtWidgets.QTableWidget(self)
            self.pushTableWidget.setColumnCount(0)
            self.pushTableWidget.setRowCount(0)
            self.vectorDbLayout.addWidget(self.pushTableWidget)
            self.pushButton = QtWidgets.QPushButton(self)
            self.vectorDbLayout.addWidget(self.pushButton)
            self.pushButton.clicked.connect(self.handlePush)
            self.vectorDbLayout.addWidget(self.pushButton)
            self.updatePullTable(self.pulledVectorManager)
            self.updatePushTable(self.pushedVectorManager)
        self.initializeText()

    def onTabChange(self):
        if self.clientHandler.isLead:
            if self.clientHandler.isConnected:
                self.pendingVectors = self.clientHandler.getPendingVectors()
            else:
                print("Could not collect pending vectors. Not connected to server.")
        self.initializeConfiguration()

    def handlePull(self):
        if self.clientHandler.isConnected:
            self.clientHandler.pullVector()
            self.triggerHelper.connectVectorConfigurationTableTrigger()
            self.triggerHelper.emitVectorConfigurationTableTrigger()
            self.pulledVectorManager = deepcopy(self.clientHandler.vectorManager)
            self.pulledVectorManager.filename = "pulledVectors.pkl"
            self.pulledVectorManager.storeVectors()
            self.updatePullTable(self.pulledVectorManager)
        else:
            print("Not connected to server.")

    def handlePush(self):
        if self.clientHandler.isConnected:
            self.pushedVectorManager = deepcopy(self.clientHandler.vectorManager)
            self.determineVectorsToPush()
            self.clientHandler.pushVector(self.pushedVectorManager)
            self.pushedVectorManager.filename = "pushedVectors.pkl"
            self.pushedVectorManager.storeVectors()
            self.updatePushTable(self.pushedVectorManager)
        else:
            print("Not connected to server.")

    def determineVectorsToPush(self):
        pushedVectors = list(self.pushedVectorManager.vectors.values())
        for vector in list(self.pulledVectorManager.vectors.values()):
            if vector.vectorName not in self.pushedVectorManager.vectors:
                self.pushedVectorManager.vectors[vector.vectorName] = deepcopy(self.pulledVectorManager.vectors[vector.vectorName])
                self.pushedVectorManager.vectors[vector.vectorName].changeSummary = "Deleted"
        for vector in pushedVectors:
            if vector.vectorName in self.pulledVectorManager.vectors:
                if vector.equals(self.pulledVectorManager.vectors[vector.vectorName]):
                    del self.pushedVectorManager.vectors[vector.vectorName]
                else:
                    vector.changeSummary = "Modified"
            else:
                vector.changeSummary = "Added"

    def updatePullTable(self, pulledVectorManager):
        vectors = pulledVectorManager.vectors
        totalRows = len(vectors)
        self.pullTableWidget.setColumnCount(len(self.colsPullTable))
        self.pullTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.pullTableWidget.setRowCount(totalRows)
        header = self.pullTableWidget.horizontalHeader()
        for colNum in range(len(self.colsPullTable)):
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsPullTable[colNum])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.pullTableWidget.setHorizontalHeaderItem(colNum, headerItem)
        rowNum = 0
        for vectorName, vector in vectors.items():
            self.pullTableWidget.setRowHeight(rowNum, 50)
            vectorNameItem = QtWidgets.QTableWidgetItem(vectorName)
            vectorNameItem.setFont(QtGui.QFont('SansSerif', 7))
            self.pullTableWidget.setItem(rowNum, self.colsPullTable.index("Vector Name"), vectorNameItem)
            vectorDescriptionItem = QtWidgets.QTableWidgetItem(vector.vectorDescription)
            vectorDescriptionItem.setFont(QtGui.QFont('SansSerif', 7))
            self.pullTableWidget.setItem(rowNum, self.colsPullTable.index("Vector Description"), vectorDescriptionItem)
            graphButton = ViewGraphButton(vector)
            graphButton.setText("View Graph")
            graphButton.setFont(QtGui.QFont('SansSerif', 7))
            self.pullTableWidget.setCellWidget(rowNum, self.colsPullTable.index("Vector Graph"), graphButton)
            rowNum += 1
        self.pullTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def updatePushTable(self, pushedVectorManager):
        vectors = pushedVectorManager.vectors
        totalRows = len(vectors)
        self.pushTableWidget.setColumnCount(len(self.colsPushTable))
        self.pushTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.pushTableWidget.setRowCount(totalRows)
        header = self.pushTableWidget.horizontalHeader()
        for colNum in range(len(self.colsPushTable)):
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsPushTable[colNum])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.pushTableWidget.setHorizontalHeaderItem(colNum, headerItem)
        rowNum = 0
        for vectorName, vector in vectors.items():
            self.pushTableWidget.setRowHeight(rowNum, 50)
            vectorNameItem = QtWidgets.QTableWidgetItem(vectorName)
            vectorNameItem.setFont(QtGui.QFont('SansSerif', 7))
            self.pushTableWidget.setItem(rowNum, self.colsPushTable.index("Vector Name"), vectorNameItem)
            vectorChangeSummaryItem = QtWidgets.QTableWidgetItem(vector.changeSummary)
            vectorChangeSummaryItem.setFont(QtGui.QFont('SansSerif', 7))
            self.pushTableWidget.setItem(rowNum, self.colsPushTable.index("Change Summary"), vectorChangeSummaryItem)
            vectorDescriptionItem = QtWidgets.QTableWidgetItem(vector.vectorDescription)
            vectorDescriptionItem.setFont(QtGui.QFont('SansSerif', 7))
            self.pushTableWidget.setItem(rowNum, self.colsPushTable.index("Vector Description"), vectorDescriptionItem)
            graphButton = ViewGraphButton(vector)
            graphButton.setText("View Graph")
            graphButton.setFont(QtGui.QFont('SansSerif', 7))
            self.pushTableWidget.setCellWidget(rowNum, self.colsPushTable.index("Vector Graph"), graphButton)
            rowNum += 1
        self.pushTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def initializeText(self):
        self.vectorDbLabel.setText("VECTOR DB CONFIGURATION")
        self.vectorDbLabel.setFont(QtGui.QFont('SansSerif', 7))
        if self.clientHandler.isLead:
            self.approvalLabel.setText("Approval sync:")
            self.approvalLabel.setFont(QtGui.QFont('SansSerif', 7))
        else:
            self.pullTableLabel.setText("Pulled Vector DB Table (Analyst):")
            self.pullTableLabel.setFont(QtGui.QFont('SansSerif', 7))
            self.pushTableLabel.setText("Pushed Vector DB Table (Analyst):")
            self.pushTableLabel.setFont(QtGui.QFont('SansSerif', 7))
            self.pushButton.setText("Push Button")
            self.pushButton.setFont(QtGui.QFont('SansSerif', 7))
            self.pullButton.setText("Pull Button")
            self.pullButton.setFont(QtGui.QFont('SansSerif', 7))

    def updateApproveTable(self, pendingVectors):
        self.colsApproveTable = ["Vector Name", "Vector Description", "Change Summary", "Graph", "Approve", "Reject"]
        totalRows = len(pendingVectors)
        self.approvalTableWidget.setColumnCount(len(self.colsApproveTable))
        self.approvalTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.approvalTableWidget.setRowCount(totalRows)
        header = self.approvalTableWidget.horizontalHeader()
        for colNum in range(len(self.colsApproveTable)):
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsApproveTable[colNum])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.approvalTableWidget.setHorizontalHeaderItem(colNum, headerItem)
        rowNum = 0
        for vectorKey, vector in pendingVectors.items():
            self.approvalTableWidget.setRowHeight(rowNum, 50)
            vectorNameItem = QtWidgets.QTableWidgetItem(vector.vectorName)
            vectorNameItem.setFont(QtGui.QFont('SansSerif', 7))
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Vector Name"), vectorNameItem)
            changeItem = QtWidgets.QTableWidgetItem(vector.changeSummary)
            changeItem.setFont(QtGui.QFont('SansSerif', 7))
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Change Summary"), changeItem)
            vectorDescriptionItem = QtWidgets.QTableWidgetItem(vector.vectorDescription)
            vectorDescriptionItem.setFont(QtGui.QFont('SansSerif', 7))
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Vector Description"), vectorDescriptionItem)
            graphButton = ViewGraphButton(vector)
            graphButton.setText("View Graph")
            graphButton.setFont(QtGui.QFont('SansSerif', 7))
            self.approvalTableWidget.setCellWidget(rowNum, self.colsApproveTable.index("Graph"), graphButton)
            approveButton = ApproveVectorButton(self.updateApproveTable, self.clientHandler, vectorKey, vector)
            approveButton.setText("Approve")
            approveButton.setFont(QtGui.QFont('SansSerif', 7))
            self.approvalTableWidget.setCellWidget(rowNum, self.colsApproveTable.index("Approve"), approveButton)
            rejectButton = ApproveVectorButton(self.updateApproveTable, self.clientHandler, vectorKey, vector)
            rejectButton.setText("Reject")
            rejectButton.setFont(QtGui.QFont('SansSerif', 7))
            self.approvalTableWidget.setCellWidget(rowNum, self.colsApproveTable.index("Reject"), rejectButton)
            rowNum += 1
        self.approvalTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

class ApproveVectorButton(QtWidgets.QPushButton):
    def __init__(self, updateApproveTable, clientHandler, vectorKey, vector):
        super(ApproveVectorButton, self).__init__()
        self.clientHandler = clientHandler
        self.vector = vector
        self.vectorKey = vectorKey
        self.updateApproveTable = updateApproveTable
        self.clicked.connect(self.handleClick)

    def handleClick(self):
        if self.clientHandler.isConnected:
            self.updateApproveTable(self.clientHandler.approveVector(self.vectorKey, self.vector))
        else:
            print("Not connected to server.")

class RejectVectorButton(QtWidgets.QPushButton):
    def __init__(self, updateApproveTable, clientHandler, vectorKey, vector):
        super(RejectVectorButton, self).__init__()
        self.clientHandler = clientHandler
        self.vector = vector
        self.vectorKey = vectorKey
        self.updateApproveTable = updateApproveTable
        self.clicked.connect(self.handleClick)

    def handleClick(self):
        if self.clientHandler.isConnected:
            self.updateApproveTable(self.clientHandler.rejectVector(self.vectorKey, self.vector))
        else:
            print("Not connected to server.")

class ViewGraphButton(QtWidgets.QPushButton):
    def __init__(self, vector):
        super(ViewGraphButton, self).__init__()
        self.vector = vector
        self.clicked.connect(self.handleClick)

    def handleClick(self):
        self.viewGraphClicked(self.vector)

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
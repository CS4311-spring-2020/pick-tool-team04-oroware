from PyQt5 import QtWidgets, QtCore
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
        self.colsPushTable = ["Vector Name", "Vector Description", "Vector Graph"]
        self.colsApproveTable = ["Source IP", "Request Timestamp", "Vector Name", "Vector Description", "Graph", "Approve"]
        self.pushedVectorManager = VectorManager()
        self.pulledVectorManager = VectorManager()
        self.pushedVectors = list()
        self.changeSummaries = list()
        self.initializeConfiguration()

    def initializeConfiguration(self):
        self.vectorDbTab = QtWidgets.QWidget()
        self.vectorDbLayout = QtWidgets.QVBoxLayout(self)
        self.vectorDbLabel = QtWidgets.QLabel(self)
        self.vectorDbLayout.addWidget(self.vectorDbLabel)
        if self.clientHandler.isLead:
            self.approvalLabel = QtWidgets.QLabel(self)
            self.vectorDbLayout.addWidget(self.approvalLabel)
            self.approvalTableWidget = QtWidgets.QTableWidget(self)
            self.approvalTableWidget.setColumnCount(0)
            self.approvalTableWidget.setRowCount(0)
            self.approvalTableWidget.setMinimumSize(1250, 1750)
            self.vectorDbLayout.addWidget(self.approvalTableWidget)
            self.updateApproveTable(self.pushedVectors, self.changeSummaries)
        else:
            self.pullTableLabel = QtWidgets.QLabel(self)
            self.vectorDbLayout.addWidget(self.pullTableLabel)
            self.pullTableWidget = QtWidgets.QTableWidget(self)
            self.pullTableWidget.setColumnCount(0)
            self.pullTableWidget.setRowCount(0)
            self.pullTableWidget.setMinimumSize(1250, 850)
            self.vectorDbLayout.addWidget(self.pullTableWidget)
            self.pullButton = QtWidgets.QPushButton(self)
            self.pullButton.clicked.connect(self.handlePull)
            self.vectorDbLayout.addWidget(self.pullButton)
            self.pushTableLabel = QtWidgets.QLabel(self)
            self.vectorDbLayout.addWidget(self.pushTableLabel)
            self.pushTableWidget = QtWidgets.QTableWidget(self)
            self.pushTableWidget.setColumnCount(0)
            self.pushTableWidget.setRowCount(0)
            self.pushTableWidget.setMinimumSize(1250, 850)
            self.vectorDbLayout.addWidget(self.pushTableWidget)
            self.pushButton = QtWidgets.QPushButton(self)
            self.vectorDbLayout.addWidget(self.pushButton)
            self.pushButton.clicked.connect(self.handlePush)
            self.vectorDbLayout.addWidget(self.pushButton)
            self.updatePullTable(self.pulledVectorManager)
            self.updatePushTable(self.pushedVectorManager)
        self.initializeText()

    def onTabChange(self):
        print("here")

    def handlePull(self):
        self.clientHandler.pullVectorDb()
        self.triggerHelper.connectVectorConfigurationTableTrigger()
        self.triggerHelper.emitVectorConfigurationTableTrigger()
        self.pulledVectorManager = deepcopy(self.clientHandler.vectorManager)
        self.updatePullTable(self.pulledVectorManager)
        self.pullButton.clicked.disconnect(self.handlePull)

    def handlePush(self):
        self.pushedVectorManager = deepcopy(self.clientHandler.vectorManager)
        self.updatePushTable(self.pushedVectorManager)

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
        self.pullTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

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

    def initializeText(self):
        self.vectorDbLabel.setText("VECTOR DB CONFIGURATION")
        if self.clientHandler.isLead:
            self.approvalLabel.setText("Approval sync:")
        else:
            self.pullTableLabel.setText("Pulled Vector DB Table (Analyst):")
            self.pushTableLabel.setText("Pushed Vector DB Table (Analyst):")
            self.pushButton.setText("Push Button")
            self.pullButton.setText("Pull Button")

    def updateApproveTable(self, pushedVectors, changeSummaries):
        self.colsApproveTable = ["Vector Name", "Vector Description", "Graph", "Approve"]
        totalRows = len(pushedVectors)
        self.approvalTableWidget.setColumnCount(len(self.colsApproveTable))
        self.approvalTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.approvalTableWidget.setRowCount(totalRows)
        header = self.approvalTableWidget.horizontalHeader()
        for colNum in range(len(self.colsApproveTable)):
            self.approvalTableWidget.setColumnWidth(colNum, 200)
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            self.approvalTableWidget.setHorizontalHeaderItem(colNum, QTableWidgetItem(self.colsApproveTable[colNum]))
        rowNum = 0
        for vectorName, vector in pushedVectors.items():
            self.approvalTableWidget.setRowHeight(rowNum, 50)
            vectorNameItem = QtWidgets.QTableWidgetItem(vectorName)
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Vector Name"), vectorNameItem)
            changeItem = QtWidgets.QTableWidgetItem(changeSummaries[rowNum])
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Change Summary"), changeItem)
            vectorDescriptionItem = QtWidgets.QTableWidgetItem(vector.vectorDescription)
            self.approvalTableWidget.setItem(rowNum, self.colsApproveTable.index("Vector Description"), vectorDescriptionItem)
            graphButton = ViewGraphButton(pushedVectors[rowNum])
            graphButton.setText("View Graph")
            self.approvalTableWidget.setCellWidget(rowNum, self.colsApproveTable.index("Vector Graph"), graphButton)
            approveButton = QtWidgets.QPushButton()
            approveButton.setText("Approve")
            self.approvalTableWidget.setCellWidget(rowNum, self.colsApproveTable.index("Approve"), approveButton)
            rowNum += 1
        self.approvalTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

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
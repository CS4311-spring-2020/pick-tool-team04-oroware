from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from functools import partial

from VectorConfigurationPopup import VectorConfigurationPopup

class VectorConfiguration(QWidget):
    def __init__(self, clientHandler, triggerHelper):
        super(VectorConfiguration, self).__init__()
        self.colsVectorConfigurationTable = ["Vector Name", "Vector Description", ""]
        self.clientHandler = clientHandler
        self.triggerHelper = triggerHelper
        self.vectorConfigurationLayout = QtWidgets.QVBoxLayout(self)
        self.vectorConfigurationLabel = QtWidgets.QLabel(self)
        self.vectorConfigurationLayout.addWidget(self.vectorConfigurationLabel)
        self.currentVectorConfigurationLabel = QtWidgets.QLabel(self)
        self.vectorConfigurationLayout.addWidget(self.currentVectorConfigurationLabel)
        self.vectorComboBoxConfiguration = QtWidgets.QComboBox(self)
        self.vectorComboBoxConfiguration.setFont(QtGui.QFont('SansSerif', 7))
        self.vectorComboBoxConfiguration.setModel(QtGui.QStandardItemModel())
        self.vectorComboBoxConfiguration.view().pressed.connect(self.handleVectorComboBoxConfiguration)
        self.vectorConfigurationLayout.addWidget(self.vectorComboBoxConfiguration)
        self.configurationVectorDescriptionLabel = QtWidgets.QLabel(self)
        self.vectorConfigurationLayout.addWidget(self.configurationVectorDescriptionLabel)
        self.configurationVectorDescriptionTextEdit = QtWidgets.QPlainTextEdit(self)
        self.configurationVectorDescriptionTextEdit.setMaximumHeight(25)
        self.vectorConfigurationLayout.addWidget(self.configurationVectorDescriptionTextEdit)
        self.addVectorButton = QtWidgets.QPushButton(self)
        self.vectorConfigurationLayout.addWidget(self.addVectorButton)
        self.addVectorButton.clicked.connect(self.handleAddVector)
        self.vectorConfigurationTableWidget = QtWidgets.QTableWidget(self)
        self.vectorConfigurationTableWidget.setColumnCount(0)
        self.vectorConfigurationTableWidget.setRowCount(0)
        self.vectorConfigurationLayout.addWidget(self.vectorConfigurationTableWidget)
        self.intializeText()

    def updateComboBox(self):
        self.vectorComboBoxConfiguration.clear()
        vectorNames = (self.clientHandler.vectorManager.vectors.keys())
        for vectorName in vectorNames:
            self.vectorComboBoxConfiguration.addItem(vectorName)

    def handleVectorComboBoxConfiguration(self, index):
        if self.vectorComboBoxConfiguration.count() > 0:
            self.configurationVectorDescriptionTextEdit.setPlainText(self.clientHandler.vectorManager.vectors[index.data()].vectorDescription)

    def updateVectorConfigurationTable(self):
        vectors = self.clientHandler.vectorManager.vectors
        totalRows = len(vectors)
        self.vectorConfigurationTableWidget.setColumnCount(len(self.colsVectorConfigurationTable))
        self.vectorConfigurationTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.vectorConfigurationTableWidget.setRowCount(totalRows)
        header = self.vectorConfigurationTableWidget.horizontalHeader()
        for colNum in range(len(self.colsVectorConfigurationTable)):
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            headerItem = QTableWidgetItem(self.colsVectorConfigurationTable[colNum])
            headerItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorConfigurationTableWidget.setHorizontalHeaderItem(colNum, headerItem)
        rowNum = 0
        for vectorName, vector in vectors.items():
            self.vectorConfigurationTableWidget.setRowHeight(rowNum, 50)
            vectorNameItem = QtWidgets.QTableWidgetItem(vectorName)
            vectorNameItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorConfigurationTableWidget.setItem(rowNum, self.colsVectorConfigurationTable.index("Vector Name"), vectorNameItem)
            vectorDescriptionItem = QtWidgets.QTableWidgetItem(vector.vectorDescription)
            vectorDescriptionItem.setFont(QtGui.QFont('SansSerif', 7))
            self.vectorConfigurationTableWidget.setItem(rowNum, self.colsVectorConfigurationTable.index("Vector Description"), vectorDescriptionItem)
            self.btn = QtWidgets.QPushButton(self)
            self.btn.setCursor(QtCore.Qt.ArrowCursor)
            self.btn.setText("Delete")
            self.btn.setFont(QtGui.QFont('SansSerif', 7))
            self.btn.clicked.connect(partial(self.deleteClicked, vectorName))
            self.vectorConfigurationTableWidget.setCellWidget(rowNum, 2, self.btn)
            rowNum += 1
        # self.vectorConfigurationTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # self.vectorConfigurationTableWidget.doubleClicked.connect(self.vectorConfigurationDoubleClicked())

    def onTabChange(self):
        self.updateVectorConfigurationTable()

    def handleAddVector(self):
        self.vectorConfigurationPopup = VectorConfigurationPopup(self.triggerHelper, self.clientHandler)
        self.vectorConfigurationPopup.setGeometry(100, 200, 200, 200)
        self.vectorConfigurationPopup.show()

    def deleteClicked(self, vectorName):
        button = self.sender()
        if button:
            row = self.vectorConfigurationTableWidget.indexAt(button.pos()).row()
            self.vectorConfigurationTableWidget.removeRow(row)
            self.clientHandler.vectorManager.deleteVector(vectorName)
            self.clientHandler.vectorManager.storeVectors()

    def intializeText(self):
        self.vectorConfigurationLabel.setText("VECTOR CONFIGURATION")
        self.vectorConfigurationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.addVectorButton.setText("Add Vector")
        self.addVectorButton.setFont(QtGui.QFont('SansSerif', 7))
        self.configurationVectorDescriptionLabel.setText("Vector Description:")
        self.configurationVectorDescriptionLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.currentVectorConfigurationLabel.setText("Current vector:")
        self.currentVectorConfigurationLabel.setFont(QtGui.QFont('SansSerif', 7))

    def vectorConfigurationDoubleClicked(self):
        pass
        #vectorConfigurationId = self.vectorConfigurationTableWidget.verticalHeaderItem(self.vectorConfigurationTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        #vectorName = self.vectorComboBoxTable.currentText()
        #vector = self.clientHandler.vectorManager.vectors[vectorName]
        #vectorConfigurationToEdit = vector.vectorConfiguration[int(vectorConfigurationId)]
        #self.editVectorConfigurationPopup = VectorConfigurationPopup(vector, vectorConfigurationToEdit, trigger)
        #self.editVectorConfigurationPopup.setGeometry(100, 200, 200, 200)
        #self.editVectorConfigurationPopup.show()
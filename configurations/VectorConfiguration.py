from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

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
        self.vectorComboBoxConfiguration.setModel(QtGui.QStandardItemModel())
        self.vectorComboBoxConfiguration.view().pressed.connect(self.handleVectorComboBoxConfiguration)
        self.vectorConfigurationLayout.addWidget(self.vectorComboBoxConfiguration)
        self.configurationVectorDescriptionLabel = QtWidgets.QLabel(self)
        self.vectorConfigurationLayout.addWidget(self.configurationVectorDescriptionLabel)
        self.configurationVectorDescriptionTextEdit = QtWidgets.QPlainTextEdit(self)
        self.vectorConfigurationLayout.addWidget(self.configurationVectorDescriptionTextEdit)
        self.deleteVectorButton = QtWidgets.QPushButton(self)
        self.vectorConfigurationLayout.addWidget(self.deleteVectorButton)
        #self.editVectorButton = QtWidgets.QPushButton(self)
        #self.vectorConfigurationLayout.addWidget(self.editVectorButton)
        self.addVectorButton = QtWidgets.QPushButton(self)
        self.vectorConfigurationLayout.addWidget(self.addVectorButton)
        self.addVectorButton.clicked.connect(self.handleAddVector)
        self.vectorConfigurationTableWidget = QtWidgets.QTableWidget(self)
        self.vectorConfigurationTableWidget.setColumnCount(0)
        self.vectorConfigurationTableWidget.setRowCount(0)
        self.vectorConfigurationTableWidget.setMinimumSize(1250, 1750)
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
            btn = QtWidgets.QPushButton('Delete')
            # self.vectorConfigurationTableWidget.setItem(rowNum, self.colsVectorConfigurationTable.index("Delete"), btn)
            btn.clicked.connect(self.deleteClicked)
            self.vectorConfigurationTableWidget.setCellWidget(0, 2, btn)
            selected = self.vectorConfigurationTableWidget.selectedItems()
        # self.vectorConfigurationTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # self.vectorConfigurationTableWidget.doubleClicked.connect(self.vectorConfigurationDoubleClicked())

    def handleAddVector(self):
        self.vectorConfigurationPopup = VectorConfigurationPopup(self.triggerHelper, self.clientHandler)
        self.vectorConfigurationPopup.setGeometry(100, 200, 200, 200)
        self.vectorConfigurationPopup.show()

    def deleteClicked(self):
        button = self.sender()
        if button:
            row = self.vectorConfigurationTableWidget.indexAt(button.pos()).row()
            self.vectorConfigurationTableWidget.removeRow(row)

    def intializeText(self):
        self.vectorConfigurationLabel.setText("VECTOR CONFIGURATION")
        self.addVectorButton.setText("Add Vector")
        self.deleteVectorButton.setText("Delete Vector")
        #self.editVectorButton.setText("Edit Vector")
        self.configurationVectorDescriptionLabel.setText("Vector Description:")
        self.currentVectorConfigurationLabel.setText("Current vector:")

    def vectorConfigurationDoubleClicked(self):
        pass
        #vectorConfigurationId = self.vectorConfigurationTableWidget.verticalHeaderItem(self.vectorConfigurationTableWidget.selectionModel().selectedIndexes()[0].row()).text()
        #vectorName = self.vectorComboBoxTable.currentText()
        #vector = self.clientHandler.vectorManager.vectors[vectorName]
        #vectorConfigurationToEdit = vector.vectorConfiguration[int(vectorConfigurationId)]
        #self.editVectorConfigurationPopup = VectorConfigurationPopup(vector, vectorConfigurationToEdit, trigger)
        #self.editVectorConfigurationPopup.setGeometry(100, 200, 200, 200)
        #self.editVectorConfigurationPopup.show()
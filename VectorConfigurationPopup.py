from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from Vector import Vector

class VectorConfigurationPopup(QWidget):
    def __init__(self, triggerHelper, clientHandler):
        super(VectorConfigurationPopup, self).__init__()
        self.triggerHelper = triggerHelper
        self.triggerHelper.connectVectorConfigurationTableTrigger()
        self.clientHandler = clientHandler
        self.layout = QVBoxLayout()
        self.vectorConfigurationLabel = QLabel()
        self.vectorConfigurationLabel.setText("Vector Name:")
        self.vectorConfigurationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.vectorConfigurationLabel)
        self.vectorConfigurationEdit = QPlainTextEdit()
        self.vectorConfigurationEdit.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.vectorConfigurationEdit)
        self.vectorConfigurationDescription = QLabel()
        self.vectorConfigurationDescription.setFont(QtGui.QFont('SansSerif', 7))
        self.vectorConfigurationDescription.setText("Vector Description: ")
        self.layout.addWidget(self.vectorConfigurationDescription)
        self.vectorConfigurationDescriptionEdit = QPlainTextEdit()
        self.vectorConfigurationDescriptionEdit.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.vectorConfigurationDescriptionEdit)
        self.saveButton = QPushButton('Add Vector', self)
        self.saveButton.setFont(QtGui.QFont('SansSerif', 7))
        self.saveButton.clicked.connect(self.onSaveClick)
        self.layout.addWidget(self.saveButton)
        self.setLayout(self.layout)
        self.setWindowTitle("Add Vector Popup")

    def onSaveClick(self):
        vector = Vector()
        vector.vectorName = self.vectorConfigurationEdit.toPlainText()
        vector.vectorDescription = self.vectorConfigurationDescriptionEdit.toPlainText()
        if len(vector.vectorName) == 0:
            print("No vector name provided.")
            return
        if len(vector.vectorDescription) == 0:
            print("No vector description provided.")
            return
        if self.clientHandler.vectorManager.addVector(vector):
            self.triggerHelper.emitVectorConfigurationTableTrigger()
            self.clientHandler.vectorManager.storeVectors()
            if self.clientHandler.isLead:
                self.clientHandler.updateVector(vector)
            self.close()
        else:
            print("Vector already exists.")
            return



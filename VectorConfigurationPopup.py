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
        self.layout.addWidget(self.vectorConfigurationLabel)
        self.vectorConfigurationEdit = QPlainTextEdit()
        self.layout.addWidget(self.vectorConfigurationEdit)
        self.vectorConfigurationDescription = QLabel()
        self.vectorConfigurationDescription.setText("Vector Description: ")
        self.layout.addWidget(self.vectorConfigurationDescription)
        self.vectorConfigurationDescriptionEdit = QPlainTextEdit()
        self.layout.addWidget(self.vectorConfigurationDescriptionEdit)
        self.saveButton = QPushButton('Add Vector', self)
        self.saveButton.clicked.connect(self.onSaveClick)
        self.layout.addWidget(self.saveButton)
        self.setLayout(self.layout)
        self.setWindowTitle("Add Vector Popup")

    def onSaveClick(self):
        vector = Vector()
        vector.vectorName = self.vectorConfigurationEdit.toPlainText()
        vector.vectorDescription = self.vectorConfigurationDescriptionEdit.toPlainText()
        if self.clientHandler.vectorManager.addVector(vector):
            self.triggerHelper.emitVectorConfigurationTableTrigger()
            self.clientHandler.vectorManager.storeVectors()
            self.close()



from PyQt5.QtWidgets import *

class VectorConfigurationPopup(QWidget):
    def __init__(self, vector, vectorConfiguration, trigger):
        super(VectorConfigurationPopup, self).__init__()
        self.vector = vector
        self.vectorConfiguration = vectorConfiguration
        self.trigger = trigger
        self.trigger.connectVectorTableTrigger()
        layout = QVBoxLayout()
        self.vectorConfigurationDescriptionLabel = QLabel()
        self.vectorConfigurationDescriptionLabel.setText("Label:")
        layout.addWidget(self.vectorConfigurationDescriptionLabel)
        self.vectorConfigurationDescriptionTextEdit = QPlainTextEdit()
        self.vectorConfigurationDescriptionTextEdit.setPlainText(self.vectorConfiguration.description)
        layout.addWidget(self.vectorConfigurationDescriptionTextEdit)
        self.deleteButtonVectorConfigurationPopup = QPushButton('Delete', self)
        self.deleteButtonVectorConfigurationPopup.clicked.connect(self.delete)
        layout.addWidget(self.deleteButtonVectorConfigurationPopup)
        self.saveButtonVectorConfigurationPopup = QPushButton('Save Changes', self)
        self.saveButtonVectorConfigurationPopup.clicked.connect(self.onSaveClick)
        layout.addWidget(self.saveButtonVectorConfigurationPopup)
        self.setLayout(layout)
        self.setWindowTitle("Vector Configuration Popup")

    def onSaveClick(self):
        self.vectorConfiguration.description = self.vectorConfigurationDescriptionTextEdit.toPlainText()
        self.trigger.emitVectorConfigurationTableEntryTrigger()
        self.trigger.emitVectorTableTrigger()
        self.close()

    def delete(self):
        self.vector.removeVectorConfiguration(self.vectorConfiguration.id)
        logEntry = self.vectorConfiguration.logEntry
        vectorIndex = logEntry.associatedVectors.index(self.vector.vectorName)
        del logEntry.associatedVectors[vectorIndex]
        self.trigger.emitVectorTableTrigger()
        self.close()


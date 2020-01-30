from PyQt5.QtWidgets import *

class SignificantEventPopup(QWidget):
    def __init__(self, vector, significantEvent, trigger):
        super(SignificantEventPopup, self).__init__()
        self.vector = vector
        self.significantEvent = significantEvent
        self.trigger = trigger
        self.trigger.connectVectorTableEntryTrigger(self.significantEvent, vector.vectorName)
        self.trigger.connectSearchLogTableEntryTrigger(self.significantEvent.logEntry)
        self.trigger.connectVectorTableTrigger()
        layout = QVBoxLayout()
        self.logEntryDescriptionLabel = QLabel()
        self.logEntryDescriptionLabel.setText("Description:")
        layout.addWidget(self.logEntryDescriptionLabel)
        self.logEntryDescriptionTextEdit = QPlainTextEdit()
        self.logEntryDescriptionTextEdit.setPlainText(self.significantEvent.logEntry.description)
        layout.addWidget(self.logEntryDescriptionTextEdit)
        self.creatorLabel = QLabel()
        self.creatorLabel.setText("Creator: " + self.significantEvent.logEntry.creator)
        layout.addWidget(self.creatorLabel)
        self.dateLabel = QLabel()
        self.dateLabel.setText("Time of Event: " + self.significantEvent.logEntry.date)
        layout.addWidget(self.dateLabel)
        self.artifactLabel = QLabel()
        self.artifactLabel.setText("Artifact: " + self.significantEvent.logEntry.artifact)
        layout.addWidget(self.artifactLabel)
        self.deleteButtonSignificantEventPopup = QPushButton('Delete', self)
        self.deleteButtonSignificantEventPopup.clicked.connect(self.delete)
        layout.addWidget(self.deleteButtonSignificantEventPopup)
        self.saveButtonSignificantEventPopup = QPushButton('Save Changes', self)
        self.saveButtonSignificantEventPopup.clicked.connect(self.onSaveClick)
        layout.addWidget(self.saveButtonSignificantEventPopup)
        self.setLayout(layout)
        self.setWindowTitle("Significant Event Edit Popup")

    def onSaveClick(self):
        self.significantEvent.logEntry.description = self.logEntryDescriptionTextEdit.toPlainText()
        self.trigger.emitVectorTableEntryTrigger()
        self.trigger.emitSearchLogTableEntryTrigger()
        self.close()

    def delete(self):
        self.vector.removeSignificantEvent(self.significantEvent.id)
        logEntry = self.significantEvent.logEntry
        vectorIndex = logEntry.associatedVectors.index(self.vector.vectorName)
        del logEntry.associatedVectors[vectorIndex]
        self.trigger.emitVectorTableTrigger()
        self.close()

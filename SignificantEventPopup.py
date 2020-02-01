from PyQt5.QtWidgets import *

class SignificantEventPopup(QWidget):
    def __init__(self, vector, significantEvent, trigger):
        super(SignificantEventPopup, self).__init__()
        self.vector = vector
        self.significantEvent = significantEvent
        self.trigger = trigger
        self.trigger.connectVectorTableTrigger()
        layout = QVBoxLayout()
        self.eventNameLabel = QLabel()
        self.eventNameLabel.setText("Name:")
        layout.addWidget(self.eventNameLabel)
        self.eventNameTextEdit = QPlainTextEdit()
        self.eventNameTextEdit.setPlainText(self.significantEvent.name)
        layout.addWidget(self.eventNameTextEdit)
        self.eventDescriptionLabel = QLabel()
        self.eventDescriptionLabel.setText("Description:")
        layout.addWidget(self.eventDescriptionLabel)
        self.eventDescriptionTextEdit = QPlainTextEdit()
        self.eventDescriptionTextEdit.setPlainText(self.significantEvent.description)
        layout.addWidget(self.eventDescriptionTextEdit)
        self.creatorLabel = QLabel()
        self.creatorLabel.setText("Creator: " + self.significantEvent.logEntry.creator)
        layout.addWidget(self.creatorLabel)
        self.typeLabel = QLabel()
        self.typeLabel.setText("Event: " + self.significantEvent.logEntry.eventType)
        layout.addWidget(self.typeLabel)
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
        self.significantEvent.name = self.eventNameTextEdit.toPlainText()
        self.significantEvent.description = self.eventDescriptionTextEdit.toPlainText()
        self.trigger.emitVectorTableTrigger()
        self.close()

    def delete(self):
        self.vector.removeSignificantEvent(self.significantEvent.id)
        logEntry = self.significantEvent.logEntry
        vectorIndex = logEntry.associatedVectors.index(self.vector.vectorName)
        del logEntry.associatedVectors[vectorIndex]
        self.trigger.emitVectorTableTrigger()
        self.close()


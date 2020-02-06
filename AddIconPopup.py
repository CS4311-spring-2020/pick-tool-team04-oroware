from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

class AddIconPopup(QWidget):
    def __init__(self, clientHandler):
        super(AddIconPopup, self).__init__()
        self.clientHandler = clientHandler
        self.layout = QVBoxLayout()
        self.nameLabel = QLabel()
        self.nameLabel.setText("Icon Name:")
        self.layout.addWidget(self.logEntryDescriptionLabel)
        self.nameTextEdit = QPlainTextEdit()
        self.layout.addWidget(self.nameTextEdit)
        self.creatorLabel = QLabel()
        self.creatorLabel.setText("Creator: " + self.logEntry.creator)
        self.layout.addWidget(self.creatorLabel)
        self.typeLabel = QLabel()
        self.typeLabel.setText("Event: " + self.logEntry.eventType)
        self.layout.addWidget(self.typeLabel)
        self.dateLabel = QLabel()
        self.dateLabel.setText("Timestamp: " + self.logEntry.date)
        self.layout.addWidget(self.dateLabel)
        self.artifactLabel = QLabel()
        self.artifactLabel.setText("Artifact: " + self.logEntry.artifact)
        self.layout.addWidget(self.artifactLabel)
        self.associationLabel = QLabel()
        self.associationLabel.setText("Associated to:")
        self.layout.addWidget(self.associationLabel)
        self.saveButton = QPushButton('Save Changes', self)
        self.saveButton.clicked.connect(self.onSaveClick)
        self.layout.addWidget(self.saveButton)
        self.setLayout(self.layout)
        self.setWindowTitle("Add Icon Popup")

    def onSaveClick(self):

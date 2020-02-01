from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

class LogEntryViewPopup(QWidget):
    def __init__(self, logEntry):
        super(LogEntryViewPopup, self).__init__()
        self.logEntry = logEntry
        self.layout = QVBoxLayout()
        self.logEntryDescriptionLabel = QLabel()
        self.logEntryDescriptionLabel.setText("Content: " + self.logEntry.description)
        self.layout.addWidget(self.logEntryDescriptionLabel)
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
        self.setLayout(self.layout)
        self.setWindowTitle("Log Entry View Popup")
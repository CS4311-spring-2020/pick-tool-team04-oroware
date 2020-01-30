from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

from LogEntry import LogEntry
from Globals import logEntryManager

class LogEntryPopup(QWidget):
    def __init__(self, vectors, logEntry, trigger):
        super(LogEntryPopup, self).__init__()
        self.vectors = vectors
        self.logEntry = logEntry
        self.trigger = trigger
        self.trigger.connectSearchLogTableEntryTrigger(logEntry)
        layout = QVBoxLayout()
        self.logEntryDescriptionLabel = QLabel()
        self.logEntryDescriptionLabel.setText("Description:")
        layout.addWidget(self.logEntryDescriptionLabel)
        self.logEntryDescriptionTextEdit = QPlainTextEdit()
        self.logEntryDescriptionTextEdit.setPlainText(self.logEntry.description)
        layout.addWidget(self.logEntryDescriptionTextEdit)
        self.creatorLabel = QLabel()
        self.creatorLabel.setText("Creator: " + self.logEntry.creator)
        layout.addWidget(self.creatorLabel)
        self.dateLabel = QLabel()
        self.dateLabel.setText("Time of Event: " + self.logEntry.date)
        layout.addWidget(self.dateLabel)
        self.artifactLabel = QLabel()
        self.artifactLabel.setText("Artifact: " + self.logEntry.artifact)
        layout.addWidget(self.artifactLabel)
        self.associationLabel = QLabel()
        self.associationLabel.setText("Associated to:")
        layout.addWidget(self.associationLabel)
        self.associationComboBox = CheckableComboBox()
        for i in range(len(self.vectors)):
            self.associationComboBox.addItem(self.vectors[i].vectorName)
            item = self.associationComboBox.model().item(i, 0)
            if self.vectors[i].vectorName in self.logEntry.associatedVectors:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
        layout.addWidget(self.associationComboBox)
        self.saveButtonLogEntryPopup = QPushButton('Save Changes', self)
        self.saveButtonLogEntryPopup.clicked.connect(self.onSaveClick)
        layout.addWidget(self.saveButtonLogEntryPopup)
        self.setLayout(layout)
        self.setWindowTitle("Log Entry Edit Popup")

    def onSaveClick(self):
        self.logEntry.description = self.logEntryDescriptionTextEdit.toPlainText()
        newVectors = list()
        for i in range(len(self.vectors)):
            item = self.associationComboBox.model().item(i, 0)
            if item.checkState() == QtCore.Qt.Checked:
                newVectors.append(self.vectors[i].vectorName)
        self.trigger.emitSearchLogTableEntryTrigger()
        logEntryManager.editLogEntryVectors(self.logEntry, newVectors)
        self.close()


class CheckableComboBox(QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)


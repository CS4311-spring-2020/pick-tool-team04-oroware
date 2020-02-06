from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

class LogEntryPopup(QWidget):
    def __init__(self, logEntry, logEntryDescriptionWidget, associatedVectorsWidget, clientHandler):
        super(LogEntryPopup, self).__init__()
        self.clientHandler = clientHandler
        self.logEntryDescriptionWidget = logEntryDescriptionWidget
        self.associatedVectorsWidget = associatedVectorsWidget
        self.logEntry = logEntry
        self.layout = QVBoxLayout()
        self.logEntryDescriptionLabel = QLabel()
        self.logEntryDescriptionLabel.setText("Content:")
        self.layout.addWidget(self.logEntryDescriptionLabel)
        self.logEntryDescriptionTextEdit = QPlainTextEdit()
        self.logEntryDescriptionTextEdit.setPlainText(logEntryDescriptionWidget.text())
        self.layout.addWidget(self.logEntryDescriptionTextEdit)
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
        self.associationComboBox = CheckableComboBox()
        for i in range(self.associatedVectorsWidget.count()):
            self.associationComboBox.addItem(self.associatedVectorsWidget.itemText(i))
            item = self.associationComboBox.model().item(i, 0)
            if self.associatedVectorsWidget.model().item(i, 0).checkState() == QtCore.Qt.Checked:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
        self.layout.addWidget(self.associationComboBox)
        self.saveButtonLogEntryPopup = QPushButton('Save Changes', self)
        self.saveButtonLogEntryPopup.clicked.connect(self.onSaveClick)
        self.layout.addWidget(self.saveButtonLogEntryPopup)
        self.setLayout(self.layout)
        self.setWindowTitle("Log Entry Edit Popup")

    def onSaveClick(self):
        global logEntryManager
        self.logEntryDescriptionWidget.setText(self.logEntryDescriptionTextEdit.toPlainText())
        self.logEntry.description = self.logEntryDescriptionTextEdit.toPlainText()
        newVectors = list()
        for i in range(self.associationComboBox.count()):
            if self.associationComboBox.model().item(i, 0).checkState() == QtCore.Qt.Checked:
                newVectors.append(self.associationComboBox.itemText(i))
            item = self.associatedVectorsWidget.model().item(i, 0)
            item.setCheckState(self.associationComboBox.model().item(i, 0).checkState())
        logEntryManager.editLogEntryVectors(self.logEntry, newVectors)
        self.close()

class CheckableComboBox(QtWidgets.QComboBox):
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
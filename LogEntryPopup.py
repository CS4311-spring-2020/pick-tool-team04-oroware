from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

class LogEntryPopup(QWidget):
    def __init__(self, logEntry, logEntryDescriptionWidget, logEntryLocationWidget, logEntryEventWidget, associatedVectorsWidget, clientHandler):
        super(LogEntryPopup, self).__init__()
        self.clientHandler = clientHandler
        self.logEntryDescriptionWidget = logEntryDescriptionWidget
        self.logEntryLocationWidget = logEntryLocationWidget
        self.logEntryEventWidget = logEntryEventWidget
        self.associatedVectorsWidget = associatedVectorsWidget
        self.logEntry = logEntry
        self.layout = QVBoxLayout()
        self.logEntryDescriptionLabel = QLabel()
        self.logEntryDescriptionLabel.setText("Content:")
        self.logEntryDescriptionLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.logEntryDescriptionLabel)
        self.logEntryDescriptionTextEdit = QPlainTextEdit()
        self.logEntryDescriptionTextEdit.setFont(QtGui.QFont('SansSerif', 7))
        self.logEntryDescriptionTextEdit.setPlainText(logEntryDescriptionWidget.text())
        self.layout.addWidget(self.logEntryDescriptionTextEdit)
        self.locationLabel = QLabel()
        self.locationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.locationLabel.setText("Location:")
        self.layout.addWidget(self.locationLabel)
        self.locationTextEdit = QPlainTextEdit()
        self.locationTextEdit.setFont(QtGui.QFont('SansSerif', 7))
        self.locationTextEdit.setPlainText(logEntryLocationWidget.text())
        self.layout.addWidget(self.locationTextEdit)
        self.creatorLabel = QLabel()
        self.creatorLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.creatorLabel.setText("Creator: " + self.logEntry.creator)
        self.layout.addWidget(self.creatorLabel)
        self.typeLabel = QLabel()
        self.typeLabel.setText("Event Type: ")
        self.typeLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.typeLabel)
        self.typeCombobox = QComboBox()
        self.typeCombobox.addItem(self.logEntry.eventType)
        self.typeCombobox.addItem("White Team")
        self.typeCombobox.addItem("Blue Team")
        self.typeCombobox.addItem("Red Team")
        if "White Team" == self.logEntry.eventType:
            self.typeCombobox.removeItem(1)
        if "Blue Team" == self.logEntry.eventType:
            self.typeCombobox.removeItem(2)
        if "Red Team" == self.logEntry.eventType:
            self.typeCombobox.removeItem(3)
        self.typeCombobox.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.typeCombobox)
        self.dateLabel = QLabel()
        self.dateLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.dateLabel.setText("Timestamp: " + self.logEntry.date)
        self.layout.addWidget(self.dateLabel)
        self.artifactLabel = QLabel()
        self.artifactLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.artifactLabel.setText("Artifact: " + self.logEntry.artifact)
        self.layout.addWidget(self.artifactLabel)
        self.associationLabel = QLabel()
        self.associationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.associationLabel.setText("Associated to:")
        self.layout.addWidget(self.associationLabel)
        self.associationComboBox = CheckableComboBox()
        self.associationComboBox.setFont(QtGui.QFont('SansSerif', 7))
        for i in range(self.associatedVectorsWidget.count()):
            self.associationComboBox.addItem(self.associatedVectorsWidget.itemText(i))
            item = self.associationComboBox.model().item(i, 0)
            if self.associatedVectorsWidget.model().item(i, 0).checkState() == QtCore.Qt.Checked:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
        self.layout.addWidget(self.associationComboBox)
        self.saveButtonLogEntryPopup = QPushButton('Save Changes', self)
        self.saveButtonLogEntryPopup.setFont(QtGui.QFont('SansSerif', 7))
        self.saveButtonLogEntryPopup.clicked.connect(self.onSaveClick)
        self.layout.addWidget(self.saveButtonLogEntryPopup)
        self.setLayout(self.layout)
        self.setWindowTitle("Log Entry Edit Popup")

    def onSaveClick(self):
        self.logEntryDescriptionWidget.setText(self.logEntryDescriptionTextEdit.toPlainText())
        self.logEntryLocationWidget.setText(self.locationTextEdit.toPlainText())
        self.logEntryEventWidget.setText(self.typeCombobox.currentText())
        self.logEntry.description = self.logEntryDescriptionTextEdit.toPlainText()
        self.logEntry.location = self.locationTextEdit.toPlainText()
        self.logEntry.eventType = self.typeCombobox.currentText()
        self.clientHandler.editLogEntry(self.logEntry)
        newVectors = list()
        for i in range(self.associationComboBox.count()):
            if self.associationComboBox.model().item(i, 0).checkState() == QtCore.Qt.Checked:
                newVectors.append(self.associationComboBox.itemText(i))
            item = self.associatedVectorsWidget.model().item(i, 0)
            item.setCheckState(self.associationComboBox.model().item(i, 0).checkState())
        self.clientHandler.editLogEntryVectors(self.logEntry, newVectors)
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
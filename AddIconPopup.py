from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

from Icon import Icon

class AddIconPopup(QWidget):
    def __init__(self, updateIconConfigurationTable, clientHandler):
        super(AddIconPopup, self).__init__()
        self.updateIconConfigurationTable = updateIconConfigurationTable
        self.clientHandler = clientHandler
        self.layout = QVBoxLayout()
        self.nameLabel = QLabel()
        self.nameLabel.setText("Icon Name:")
        self.nameLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.nameLabel)
        self.nameTextEdit = QPlainTextEdit()
        self.nameTextEdit.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.nameTextEdit)
        self.sourceLabel = QLabel()
        self.sourceLabel.setText("Source: ")
        self.sourceLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.sourceLabel)
        self.fileDialog = QFileDialog()
        self.fileDialog.setFileMode(QFileDialog.AnyFile)
        self.layout.addWidget(self.fileDialog)
        self.saveButton = QPushButton('Add Icon', self)
        self.saveButton.setFont(QtGui.QFont('SansSerif', 7))
        self.saveButton.clicked.connect(self.onSaveClick)
        self.layout.addWidget(self.saveButton)
        self.setLayout(self.layout)
        self.setWindowTitle("Add Icon Popup")


    def onSaveClick(self):
        icon = Icon()
        icon.name = self.nameTextEdit.toPlainText()
        if len(icon.name) == 0:
            print("No icon name provided.")
            return
        icon.source = self.fileDialog.selectedFiles()[0]
        icon.location = self.fileDialog.selectedFiles()[0]
        if len(icon.source) == 0:
            print("No source icon file provided.")
            return
        if self.clientHandler.iconManager.addIcon(icon):
            self.updateIconConfigurationTable()
            self.close()
        else:
            self.updateIconConfigurationTable()
            print("Choose different icon name.")
            return

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

from Icon import Icon


class AddIconPopup(QWidget):
    def __init__(self, triggerHelper, clientHandler):
        super(AddIconPopup, self).__init__()
        self.triggerHelper = triggerHelper
        self.triggerHelper.connectIconTableTrigger()
        self.clientHandler = clientHandler
        self.layout = QVBoxLayout()
        self.nameLabel = QLabel()
        self.nameLabel.setText("Icon Name:")
        self.layout.addWidget(self.nameLabel)
        self.nameTextEdit = QPlainTextEdit()
        self.layout.addWidget(self.nameTextEdit)
        self.sourceLabel = QLabel()
        self.sourceLabel.setText("Source: ")
        self.layout.addWidget(self.sourceLabel)
        self.fileDialog = QFileDialog()
        self.fileDialog.setFileMode(QFileDialog.AnyFile)
        self.layout.addWidget(self.fileDialog)
        self.saveButton = QPushButton('Add Icon', self)
        self.saveButton.clicked.connect(self.onSaveClick)
        self.layout.addWidget(self.saveButton)
        self.setLayout(self.layout)
        self.setWindowTitle("Add Icon Popup")

    def onSaveClick(self):
        icon = Icon()
        icon.name = self.nameTextEdit.toPlainText()
        icon.source = self.fileDialog.selectedFiles()[0]
        if self.clientHandler.iconManager.addIcon(icon):
            self.triggerHelper.emitIconTableTrigger()
            self.close()
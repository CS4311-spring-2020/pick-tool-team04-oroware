from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *


class ErrorPopup(QWidget):
    def __init__(self, errorMessage):
        super(ErrorPopup, self).__init__()
        self.errorMessage = errorMessage
        self.layout = QVBoxLayout()
        self.nameLabel = QLabel()
        self.nameLabel.setText(self.errorMessage)
        self.nameLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.nameLabel)
        self.okButton = QPushButton('OK', self)
        self.okButton.setFont(QtGui.QFont('SansSerif', 7))
        self.okButton.clicked.connect(self.onOkClick)  # User clicks OK to close the error popup
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)
        self.setWindowTitle("Error")

    def displayPopup(self):
        self.setGeometry(700, 400, 300, 100)
        self.show()

    def onOkClick(self):
        self.close()
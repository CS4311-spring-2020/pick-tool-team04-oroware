from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget


class LogFileConfiguration(QWidget):
    def __init__(self, clientHandler):
        super(LogFileConfiguration, self).__init__()
        self.clientHandler = clientHandler
        self.logFileConfigurationLayout = QtWidgets.QVBoxLayout(self)
        self.logFileTableLabel = QtWidgets.QLabel(self)
        self.logFileConfigurationLayout.addWidget(self.logFileTableLabel)
        self.logFileTableWidget = QtWidgets.QTableWidget(self)
        self.logFileTableWidget.setColumnCount(0)
        self.logFileTableWidget.setRowCount(0)
        self.logFileTableWidget.setMinimumSize(1250, 1750)
        self.logFileConfigurationLayout.addWidget(self.logFileTableWidget)
        self.enforcementActionReportTableLabel = QtWidgets.QLabel(self)
        self.logFileConfigurationLayout.addWidget(self.enforcementActionReportTableLabel)
        self.enforcementActionReportTableWidget = QtWidgets.QTableWidget(self)
        self.enforcementActionReportTableWidget.setColumnCount(0)
        self.enforcementActionReportTableWidget.setRowCount(0)
        self.enforcementActionReportTableWidget.setMinimumSize(1250, 1750)
        self.logFileConfigurationLayout.addWidget(self.enforcementActionReportTableWidget)
        self.initializeText()

    def initializeText(self):
        self.enforcementActionReportTableLabel.setText("Enforcement Action Report Table")
        self.logFileTableLabel.setText("Log File Table")



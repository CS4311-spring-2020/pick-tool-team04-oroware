from datetime import datetime

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QWidget

from ErrorPopup import ErrorPopup


class TeamConfiguration(QWidget):
    def __init__(self, clientHandler):
        super(TeamConfiguration, self).__init__()
        self.clientHandler = clientHandler
        self.teamConfigurationTab = QtWidgets.QWidget()
        self.teamConfigurationTabLayout = QtWidgets.QVBoxLayout(self)

        # Initialize Team Configuration
        self.teamConfiguration = QtWidgets.QFrame(self)
        self.teamConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        self.teamConfigurationLayout = QtWidgets.QVBoxLayout(self.teamConfiguration)
        self.teamConfigurationLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.teamConfigurationLabel)
        self.leadCheckBox = QtWidgets.QCheckBox(self.teamConfiguration)
        if self.clientHandler.isLead:
            self.leadCheckBox.setCheckState(QtCore.Qt.Checked)
        self.leadCheckBox.clicked.connect(self.setLead)
        self.teamConfigurationLayout.addWidget(self.leadCheckBox)
        self.connectionLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.connectionLabel)
        self.leadStatusLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.leadStatusLabel)
        self.leadLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.leadLabel)
        self.leadTextEdit = QtWidgets.QTextEdit(self.teamConfiguration)
        self.leadTextEdit.setMaximumHeight(30)
        if self.clientHandler.serverIp != None:
            self.leadTextEdit.setText(self.clientHandler.serverIp)
        self.teamConfigurationLayout.addWidget(self.leadTextEdit)
        self.connectButton = QtWidgets.QPushButton(self.teamConfiguration)
        self.connectButton.clicked.connect(self.connectToServer)
        self.teamConfigurationLayout.addWidget(self.connectButton)
        self.teamConfigurationTabLayout.addWidget(self.teamConfiguration)

        # Initialize Event Configuration
        self.eventConfiguration = QtWidgets.QFrame(self)
        self.eventConfiguration.setFrameShape(QtWidgets.QFrame.Box)
        self.eventConfigurationLayout = QtWidgets.QVBoxLayout(self.eventConfiguration)
        self.eventConfigurationLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventConfigurationLabel)
        self.eventNameLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventNameLabel)
        self.eventNameTextEdit = QtWidgets.QTextEdit(self.eventConfiguration)
        self.eventNameTextEdit.setMaximumHeight(25)
        self.eventConfigurationLayout.addWidget(self.eventNameTextEdit)
        self.eventDescriptionLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventDescriptionLabel)
        self.eventDescriptionTextEdit = QtWidgets.QTextEdit(self.eventConfiguration)
        self.eventDescriptionTextEdit.setMaximumHeight(25)
        self.eventConfigurationLayout.addWidget(self.eventDescriptionTextEdit)
        self.startEventConfigurationLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.startEventConfigurationLabel)
        self.startEventConfigurationDateEdit = QtWidgets.QDateTimeEdit(self.eventConfiguration)
        self.startEventConfigurationDateEdit.setDisplayFormat("M/d/yyyy hh:mm A")
        self.startEventConfigurationDateEdit.setFont(QtGui.QFont('SansSerif', 7))
        self.startEventConfigurationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.eventConfigurationLayout.addWidget(self.startEventConfigurationDateEdit)
        self.endEventConfigurationLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.endEventConfigurationLabel)
        self.endEventConfigurationDateEdit = QtWidgets.QDateTimeEdit(self.eventConfiguration)
        self.endEventConfigurationDateEdit.setDisplayFormat("M/d/yyyy hh:mm A")
        self.endEventConfigurationDateEdit.setFont(QtGui.QFont('SansSerif', 7))
        self.eventConfigurationLayout.addWidget(self.endEventConfigurationDateEdit)
        self.teamConfigurationTabLayout.addWidget(self.eventConfiguration)
        self.saveEventButton = QtWidgets.QPushButton(self.eventConfiguration)
        self.saveEventButton.clicked.connect(self.handleSaveEvent)
        self.eventConfigurationLayout.addWidget(self.saveEventButton)
        self.intializeText()

    def connectToServer(self):
        ipAddress = self.leadTextEdit.toPlainText()
        self.clientHandler.serverIp = ipAddress
        if self.clientHandler.connectToServer():
            self.connectionLabel.setText("Connection Status: Connected to Server" if self.clientHandler.isConnected else "Connection Status: Not Connected to Server ")
            self.leadStatusLabel.setText("Lead Status: Lead Exists" if self.clientHandler.hasLead else "Lead Status: No Lead Exists")
            self.clientHandler.storeServerIp()

    def handleSaveEvent(self):
        eventConfig = self.clientHandler.eventConfig
        if (datetime.strptime(self.endEventConfigurationDateEdit.text(), "%m/%d/%Y %I:%M %p") <= datetime.strptime(self.startEventConfigurationDateEdit.text(), "%m/%d/%Y %I:%M %p")):
            print("Invalid start or end timestamp.")  # This can be removed now that error popup are implemented
            self.errorPopup = ErrorPopup("Invalid Date Range")
            self.errorPopup.displayPopup()
            return
        if len(self.eventNameTextEdit.toPlainText()) == 0:
            print("Must enter event name.")
            self.errorPopup = ErrorPopup("Event Name Required")
            self.errorPopup.displayPopup()
            return
        if len(self.eventDescriptionTextEdit.toPlainText()) == 0:
            print("Must enter event description.")
            self.errorPopup = ErrorPopup("Event Description Required")
            self.errorPopup.displayPopup()
            return
        eventConfig.eventStartTime = self.startEventConfigurationDateEdit.text()
        eventConfig.eventEndTime = self.endEventConfigurationDateEdit.text()
        eventConfig.eventDescription = self.eventDescriptionTextEdit.toPlainText()
        eventConfig.eventName = self.eventNameTextEdit.toPlainText()
        self.clientHandler.updateEventConfig()

    def setLead(self):
        if self.clientHandler.isConnected:
            if self.clientHandler.hasLead:
                if self.clientHandler.isLead:
                    self.leadCheckBox.setCheckState(QtCore.Qt.Unchecked)
                    self.clientHandler.releaseLead()
                else:
                    self.leadCheckBox.setCheckState(QtCore.Qt.Unchecked)
            else:
                self.clientHandler.setLead()
        else:
            print("Not connected to server.")
        self.intializeText()

    def intializeText(self):
        self.eventNameLabel.setText("Event name: ")
        self.eventNameLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.connectButton.setText("Connect")
        self.connectButton.setFont(QtGui.QFont('SansSerif', 7))
        self.startEventConfigurationLabel.setText("Event start timestamp:")
        self.startEventConfigurationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.leadLabel.setText("Server's IP Address: ")
        self.leadLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.leadCheckBox.setText("Lead: ")
        self.leadCheckBox.setFont(QtGui.QFont('SansSerif', 7))
        self.teamConfigurationLabel.setText("TEAM CONFIGURATION")
        self.teamConfigurationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.eventConfigurationLabel.setText("EVENT CONFIGURATION")
        self.eventConfigurationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.saveEventButton.setText("Save Event")
        self.saveEventButton.setFont(QtGui.QFont('SansSerif', 7))
        self.endEventConfigurationLabel.setText("Event end timestamp:")
        self.endEventConfigurationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.saveEventButton.setText("Save Event")
        self.saveEventButton.setFont(QtGui.QFont('SansSerif', 7))
        self.eventDescriptionLabel.setText("Event description: ")
        self.eventDescriptionLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.connectionLabel.setText("Connection Status: Connected to Server" if self.clientHandler.isConnected else "Connection Status: Not Connected to Server ")
        self.connectionLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.leadStatusLabel.setText("Lead Status: Lead Exists" if self.clientHandler.hasLead else "Lead Status: No Lead Exists")
        self.leadStatusLabel.setFont(QtGui.QFont('SansSerif', 7))
        eventConfig = self.clientHandler.eventConfig
        if eventConfig.eventEndTime != None:
            self.endEventConfigurationDateEdit.setDateTime(QDateTime.fromString(eventConfig.eventEndTime, "M/d/yyyy h:mm A"))
            self.endEventConfigurationDateEdit.setFont(QtGui.QFont('SansSerif', 7))
        if eventConfig.eventStartTime != None:
            self.startEventConfigurationDateEdit.setDateTime(QDateTime.fromString(eventConfig.eventStartTime,"M/d/yyyy h:mm A"))
            self.startEventConfigurationDateEdit.setFont(QtGui.QFont('SansSerif', 7))
        if eventConfig.eventName != None:
            self.eventNameTextEdit.setText(eventConfig.eventName)
            self.eventNameTextEdit.setFont(QtGui.QFont('SansSerif', 7))
        if eventConfig.eventDescription != None:
            self.eventDescriptionTextEdit.setText(eventConfig.eventDescription)
            self.eventDescriptionTextEdit.setFont(QtGui.QFont('SansSerif', 7))
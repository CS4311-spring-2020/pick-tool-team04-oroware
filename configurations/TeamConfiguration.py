from datetime import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QWidget


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
        self.leadLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.leadLabel)
        self.leadTextEdit = QtWidgets.QTextEdit(self.teamConfiguration)
        self.leadTextEdit.setMaximumHeight(40)
        self.teamConfigurationLayout.addWidget(self.leadTextEdit)
        self.connectButton = QtWidgets.QPushButton(self.teamConfiguration)
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
        self.eventNameTextEdit.setMaximumHeight(40)
        self.eventConfigurationLayout.addWidget(self.eventNameTextEdit)
        self.eventDescriptionLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventDescriptionLabel)
        self.eventDescriptionTextEdit = QtWidgets.QTextEdit(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventDescriptionTextEdit)
        self.startEventConfigurationLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.startEventConfigurationLabel)
        self.startEventConfigurationDateEdit = QtWidgets.QDateTimeEdit(self.eventConfiguration)
        self.startEventConfigurationDateEdit.setDisplayFormat("M/d/yyyy hh:mm A")
        self.eventConfigurationLayout.addWidget(self.startEventConfigurationDateEdit)
        self.endEventConfigurationLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.endEventConfigurationLabel)
        self.endEventConfigurationDateEdit = QtWidgets.QDateTimeEdit(self.eventConfiguration)
        self.endEventConfigurationDateEdit.setDisplayFormat("M/d/yyyy hh:mm A")
        self.eventConfigurationLayout.addWidget(self.endEventConfigurationDateEdit)
        self.teamConfigurationTabLayout.addWidget(self.eventConfiguration)
        self.saveEventButton = QtWidgets.QPushButton(self.eventConfiguration)
        self.saveEventButton.clicked.connect(self.handleSaveEvent)
        self.eventConfigurationLayout.addWidget(self.saveEventButton)
        self.intializeText()

    def handleSaveEvent(self):
        eventConfig = self.clientHandler.eventConfig
        if (datetime.strptime(self.endEventConfigurationDateEdit.text(), "%m/%d/%Y %I:%M %p") <= datetime.strptime(self.startEventConfigurationDateEdit.text(), "%m/%d/%Y %I:%M %p")):
            print("Invalid start or end timestamp.")
            return
        if len(self.eventNameTextEdit.toPlainText()) == 0:
            print("Must enter event name.")
            return
        if len(self.eventDescriptionTextEdit.toPlainText()) == 0:
            print("Must enter event description.")
            return
        eventConfig.eventStartTime = self.startEventConfigurationDateEdit.text()
        eventConfig.eventEndTime = self.endEventConfigurationDateEdit.text()
        eventConfig.eventDescription = self.eventDescriptionTextEdit.toPlainText()
        eventConfig.eventName = self.eventNameTextEdit.toPlainText()
        self.clientHandler.updateEventConfig()

    def setLead(self):
        if self.clientHandler.hasLead:
            if self.clientHandler.isLead:
                self.leadCheckBox.setCheckState(QtCore.Qt.Unchecked)
                self.clientHandler.releaseLead()
            else:
                self.leadCheckBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.clientHandler.setLead()

    def intializeText(self):
        self.eventNameLabel.setText("Event name: ")
        self.connectButton.setText("Connect")
        self.startEventConfigurationLabel.setText("Event start timestamp:")
        self.leadLabel.setText("Server's IP Address: ")
        self.leadCheckBox.setText("Lead: ")
        self.teamConfigurationLabel.setText("TEAM CONFIGURATION")
        self.eventConfigurationLabel.setText("EVENT CONFIGURATION")
        self.saveEventButton.setText("Save Event")
        self.leadCheckBox.setText("Lead")
        self.endEventConfigurationLabel.setText("Event end timestamp:")
        self.saveEventButton.setText("Save Event")
        self.eventDescriptionLabel.setText("Event description: ")
        eventConfig = self.clientHandler.eventConfig
        if eventConfig.eventEndTime != None:
            self.endEventConfigurationDateEdit.setDateTime(QDateTime.fromString(eventConfig.eventEndTime, "M/d/yyyy h:mm A"))
        if eventConfig.eventStartTime != None:
            self.startEventConfigurationDateEdit.setDateTime(QDateTime.fromString(eventConfig.eventStartTime,"M/d/yyyy h:mm A"))
        if eventConfig.eventName != None:
            self.eventNameTextEdit.setText(eventConfig.eventName)
        if eventConfig.eventDescription != None:
            self.eventDescriptionTextEdit.setText(eventConfig.eventDescription)
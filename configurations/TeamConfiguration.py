from PyQt5 import QtWidgets, QtCore
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
        self.teamConfigurationLayout.addWidget(self.leadTextEdit)
        self.establishedConnectionsLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.establishedConnectionsLabel)
        self.numConnectionsLabel = QtWidgets.QLabel(self.teamConfiguration)
        self.teamConfigurationLayout.addWidget(self.numConnectionsLabel)
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
        self.eventConfigurationLayout.addWidget(self.eventNameTextEdit)
        self.eventDescriptionLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventDescriptionLabel)
        self.eventDescriptionTextEdit = QtWidgets.QTextEdit(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.eventDescriptionTextEdit)
        self.startEventConfigurationLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.startEventConfigurationLabel)
        self.startEventConfigurationDateEdit = QtWidgets.QDateTimeEdit(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.startEventConfigurationDateEdit)
        self.endEventConfigurationLabel = QtWidgets.QLabel(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.endEventConfigurationLabel)
        self.endEventConfigurationDateEdit = QtWidgets.QDateTimeEdit(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.endEventConfigurationDateEdit)
        self.teamConfigurationTabLayout.addWidget(self.eventConfiguration)
        self.saveEventButton = QtWidgets.QPushButton(self.eventConfiguration)
        self.eventConfigurationLayout.addWidget(self.saveEventButton)
        self.intializeText()

    def setLead(self):
        if self.clientHandler.hasLead:
            if self.clientHandler.isLead:
                self.leadCheckBox.setCheckState(QtCore.Qt.Checked)
                self.clientHandler.releaseLead()
            else:
                self.leadCheckBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            self.clientHandler.setLead()

    def intializeText(self):
        self.eventNameLabel.setText("Event name: ")
        self.connectButton.setText("Connect")
        self.startEventConfigurationLabel.setText("Event start timestamp:")
        self.leadLabel.setText("Lead's IP Address: ")
        self.leadCheckBox.setText("Lead: ")
        self.teamConfigurationLabel.setText("TEAM CONFIGURATION")
        self.eventConfigurationLabel.setText("EVENT CONFIGURATION")
        self.saveEventButton.setText("Save Event")
        self.leadCheckBox.setText("Lead")
        self.establishedConnectionsLabel.setText("No. of established connections to the lead’s IP address: " + str(self.clientHandler.establishedConnections))
        self.numConnectionsLabel.setText("No. of connections to the lead’s IP address: " + str(self.clientHandler.numConnections))
        self.endEventConfigurationLabel.setText("Event end timestamp:")
        self.saveEventButton.setText("Save Event")
        self.eventDescriptionLabel.setText("Event description: ")
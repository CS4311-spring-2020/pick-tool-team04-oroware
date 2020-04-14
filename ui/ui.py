from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
import sys
from ClientHandler import ClientHandler
from configurations.EditVectorConfiguration import EditVectorConfiguration
from configurations.IconConfiguration import IconConfiguration
from configurations.LogEntryConfiguration import LogEntryConfiguration
from configurations.IngestionConfiguration import IngestionConfiguration
from configurations.TeamConfiguration import TeamConfiguration
from configurations.VectorConfiguration import VectorConfiguration
from configurations.VectorDbConfiguration import VectorDbConfiguration


class Ui_PICK(object):

    def setupMainWindow(self, PICK):
        self.mainWindow = QtWidgets.QWidget(PICK)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainWindow)

    def setupTabWidget(self):
        self.tabWidget = QtWidgets.QTabWidget(self.mainWindow)

    def setupTeamTab(self):
        self.teamConfigurationTab = TeamConfiguration(self.clientHandler)
        self.tabWidget.addTab(self.teamConfigurationTab, "")

    def setupSearchLogsTab(self):
        self.searchLogsTab = LogEntryConfiguration(self.clientHandler)
        self.tabWidget.addTab(self.searchLogsTab, "")

    def setupVectorDbTab(self):
        triggerHelper = TriggerHelper()
        self.vectorDbTab = VectorDbConfiguration(self.clientHandler, triggerHelper)
        self.tabWidget.addTab(self.vectorDbTab, "")

    def handleVectorConfigurationTableTrigger(self):
        self.vectorConfigurationTab.updateVectorConfigurationTable()
        self.updateVectorComboBoxes()
        self.searchLogsTab.updateLogTable()

    def setupEditVectorTab(self):
        triggerHelper = TriggerHelper()
        self.editVectorTab = EditVectorConfiguration(self.clientHandler, triggerHelper)
        self.tabWidget.addTab(self.editVectorTab, "")
        self.tabWidget.currentChanged.connect(self.onTabChange)

    def setupIngestionConfigurationTab(self):
        self.IngestionConfigurationTab = IngestionConfiguration(self.clientHandler)
        self.tabWidget.addTab(self.IngestionConfigurationTab, "")

    def setupVectorConfigurationTab(self):
        triggerHelper = TriggerHelper()
        self.vectorConfigurationTab = VectorConfiguration(self.clientHandler, triggerHelper)
        self.vectorConfigurationTab.updateVectorConfigurationTable()
        self.tabWidget.addTab(self.vectorConfigurationTab, "")

    def setupIconConfigurationTab(self):
        self.iconConfigurationTab = IconConfiguration(self.clientHandler)
        self.iconConfigurationTab.updateIconConfigurationTable()
        self.tabWidget.addTab(self.iconConfigurationTab, "")

    def handleVectorTableEntryUpdate(self, significantEvent, vectorName):
        self.editVectorTab.handleVectorTableEntryUpdate(significantEvent, vectorName)

    def handleSearchLogTableEntryUpdate(self, logEntry):
        self.editVectorTab.handleSearchLogTableEntryUpdate(logEntry)

    def handleRelationshipTableEntryUpdate(self, relationship, vectorName):
        self.editVectorTab.handleRelationshipTableEntryUpdate(relationship, vectorName)

    def onTabChange(self):
        self.updateVectorComboBoxes()
        if self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.editVectorTab):
            self.clientHandler.requestIcons()
            self.editVectorTab.onTabChange()
        elif self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.iconConfigurationTab):
            self.iconConfigurationTab.onTabChange()
        elif self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.vectorConfigurationTab):
            self.vectorConfigurationTab.onTabChange()
        elif self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.vectorDbTab):
            self.vectorDbTab.onTabChange()
        elif self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.teamConfigurationTab):
            self.clientHandler.requestEventConfig()
        elif self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.searchLogsTab):
            self.searchLogsTab.updateLogTable()
        elif self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.IngestionConfigurationTab):
            self.IngestionConfigurationTab.updateLogFileTable()

    def handleRelationshipTableTrigger(self):
        self.editVectorTab.handleRelationshipTableTrigger()

    def handleVectorGraphTrigger(self):
        self.editVectorTab.handleVectorGraphTrigger()

    def updateVectorComboBoxes(self):
        self.vectorConfigurationTab.updateComboBox()
        self.editVectorTab.updateComboBox()

    def setupUi(self, PICK):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        PICK.setSizePolicy(sizePolicy)

        self.clientHandler = ClientHandler()
        if self.clientHandler.isLead:
            self.clientHandler.pullVector()
        else:
            self.clientHandler.vectorManager.retrieveVectors()

        self.setupMainWindow(PICK)
        self.setupTabWidget()
        self.setupTeamTab()
        self.setupIngestionConfigurationTab()
        # self.setupDirectoryTab()
        self.setupSearchLogsTab()
        self.setupVectorConfigurationTab()
        self.setupIconConfigurationTab()
        self.setupEditVectorTab()
        self.setupVectorDbTab()

        self.updateVectorComboBoxes()

        self.verticalLayout.addWidget(self.tabWidget)

        PICK.setCentralWidget(self.mainWindow)
        self.intializeText(PICK)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PICK)

    def intializeText(self, PICK):
        PICK.setWindowTitle("PICK Tool")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.teamConfigurationTab), "Team and Event Configuration")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.IngestionConfigurationTab), "Ingestion Configuration")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.vectorConfigurationTab), "Vector Configuration")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.iconConfigurationTab), "Icon Configuration")
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.directoryTab), "Directory Configuration")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.editVectorTab), "Edit Vector")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.searchLogsTab), "Search Logs")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.vectorDbTab), "Vector DB Configuration")

class TriggerHelper(QObject):
    updateRelationshipTableTrigger = pyqtSignal()
    updateVectorGraphTrigger = pyqtSignal()
    updateVectorTableEntryTrigger = pyqtSignal()
    updateSearchLogTableEntryTrigger = pyqtSignal()
    updateRelationshipTableEntryTrigger = pyqtSignal()
    updateVectorTableTrigger = pyqtSignal()
    updateIconTableTrigger = pyqtSignal()
    updateVectorConfigurationTableTrigger = pyqtSignal()

    def connectRelationshipTableTrigger(self):
        self.updateRelationshipTableTrigger.connect(ui.handleRelationshipTableTrigger)

    def connectVectorConfigurationTableTrigger(self):
        self.updateVectorConfigurationTableTrigger.connect(ui.handleVectorConfigurationTableTrigger)

    def connectIconTableTrigger(self):
        self.updateIconTableTrigger.connect(ui.iconConfigurationTab.updateIconConfigurationTable)

    def connectVectorGraphTrigger(self):
        self.updateVectorGraphTrigger.connect(ui.handleVectorGraphTrigger)

    def connectVectorTableTrigger(self):
        self.updateVectorTableTrigger.connect(ui.onTabChange)

    def connectVectorTableEntryTrigger(self, significantEvent, vectorName):
        self.updateVectorTableEntryTrigger.connect(lambda: ui.handleVectorTableEntryUpdate(significantEvent, vectorName))

    def connectSearchLogTableEntryTrigger(self, logEntry):
        self.updateSearchLogTableEntryTrigger.connect(lambda: ui.handleSearchLogTableEntryUpdate(logEntry))

    def connectRelationshipTableEntryTrigger(self, logEntry, vectorName):
        self.updateRelationshipTableEntryTrigger.connect(lambda: ui.handleRelationshipTableEntryUpdate(logEntry, vectorName))

    def emitIconTableTrigger(self):
        self.updateIconTableTrigger.emit()

    def emitVectorGraphTrigger(self):
        self.updateVectorGraphTrigger.emit()

    def emitRelationshipTableTrigger(self):
        self.updateRelationshipTableTrigger.emit()

    def emitRelationshipTableEntryTrigger(self):
        self.updateRelationshipTableEntryTrigger.emit()

    def emitVectorTableTrigger(self):
        self.updateVectorTableTrigger.emit()

    def emitVectorTableEntryTrigger(self):
        self.updateVectorTableEntryTrigger.emit()

    def emitSearchLogTableEntryTrigger(self):
        self.updateSearchLogTableEntryTrigger.emit()

    def emitVectorConfigurationTableTrigger(self):
        self.updateVectorConfigurationTableTrigger.emit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PICK = QtWidgets.QMainWindow()
    ui = Ui_PICK()
    ui.setupUi(PICK)
    PICK.show()
    sys.exit(app.exec_())
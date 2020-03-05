from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDataStream, QIODevice
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from functools import partial

from AddIconPopup import AddIconPopup

class IconConfiguration(QWidget):

    def __init__(self, clientHandler):
        super(IconConfiguration, self).__init__()
        self.colsIconConfigurationTable = ["Icon Name", "Icon Source", "Icon Preview", ""]
        self.iconConfigurationLayout = QtWidgets.QVBoxLayout(self)
        self.iconConfigurationLabel = QtWidgets.QLabel(self)
        self.iconConfigurationLayout.addWidget(self.iconConfigurationLabel)
        self.addIconButton = QtWidgets.QPushButton(self)
        self.addIconButton.clicked.connect(self.handleAddIcon)
        self.iconConfigurationLayout.addWidget(self.addIconButton)
        self.iconConfigurationTableWidget = QtWidgets.QTableWidget(self)
        self.iconConfigurationTableWidget.setColumnCount(0)
        self.iconConfigurationTableWidget.setRowCount(0)
        self.iconConfigurationTableWidget.setMinimumSize(1250, 1750)
        self.iconConfigurationLayout.addWidget(self.iconConfigurationTableWidget)
        self.clientHandler = clientHandler
        self.intializeText()

    def intializeText(self):
        self.iconConfigurationLabel.setText("ICON CONFIGURATION")
        self.addIconButton.setText("Add Icon")

    def onTabChange(self):
        self.clientHandler.requestIcons()
        self.updateIconConfigurationTable()

    def updateIconConfigurationTable(self):
        icons = self.clientHandler.iconManager.icons
        totalRows = len(icons)
        self.iconConfigurationTableWidget.setColumnCount(len(self.colsIconConfigurationTable))
        self.iconConfigurationTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.iconConfigurationTableWidget.setRowCount(totalRows)
        header = self.iconConfigurationTableWidget.horizontalHeader()
        for colNum in range(len(self.colsIconConfigurationTable)):
            self.iconConfigurationTableWidget.setColumnWidth(colNum, 200)
            header.setSectionResizeMode(colNum, QtWidgets.QHeaderView.Stretch)
            self.iconConfigurationTableWidget.setHorizontalHeaderItem(colNum, QTableWidgetItem(
                self.colsIconConfigurationTable[colNum]))
        rowNum = 0
        for iconName, icon in icons.items():
            self.iconConfigurationTableWidget.setRowHeight(rowNum, 50)
            iconNameItem = QtWidgets.QTableWidgetItem(iconName)
            self.iconConfigurationTableWidget.setItem(rowNum, self.colsIconConfigurationTable.index("Icon Name"),
                                                      iconNameItem)
            iconSourceItem = QtWidgets.QTableWidgetItem(icon.source)
            self.iconConfigurationTableWidget.setItem(rowNum, self.colsIconConfigurationTable.index("Icon Source"),
                                                      iconSourceItem)
            viewIconButton = ViewIconButton(iconName, icon.pixmapByteArray)
            viewIconButton.setText("View Icon")
            self.iconConfigurationTableWidget.setCellWidget(rowNum,
                                                            self.colsIconConfigurationTable.index("Icon Preview"),
                                                            viewIconButton)
            icon.rowIndexInTable = rowNum
            self.btn = QtWidgets.QPushButton(self)
            self.btn.setCursor(QtCore.Qt.ArrowCursor)
            self.btn.setText("Delete")
            self.btn.clicked.connect(partial(self.deleteClicked, iconName))
            self.iconConfigurationTableWidget.setCellWidget(rowNum, 3, self.btn)
            rowNum += 1
        # self.iconConfigurationTableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def handleAddIcon(self):
        self.addIconPopup = AddIconPopup(self.updateIconConfigurationTable, self.clientHandler)
        self.addIconPopup.setGeometry(100, 200, 200, 200)
        self.addIconPopup.show()

    def deleteClicked(self, iconName):
        button = self.sender()
        if button:
            row = self.iconConfigurationTableWidget.indexAt(button.pos()).row()
            self.iconConfigurationTableWidget.removeRow(row)
            self.clientHandler.iconManager.deleteIcon(iconName)
            self.clientHandler.iconManager.storeIcons()


class ViewIconButton(QtWidgets.QPushButton):
    def __init__(self, name, pixmapByteArray):
        super(ViewIconButton, self).__init__()
        self.name = name
        self.pixmap = QPixmap()
        stream = QDataStream(pixmapByteArray, QIODevice.ReadOnly)
        stream >> self.pixmap
        self.clicked.connect(self.handleClick)

    def viewIconClicked(self, name, pixmap):
        self.labelImageDisplay = QtWidgets.QLabel()
        self.labelImageDisplay.setWindowTitle(name)
        self.labelImageDisplay.setPixmap(pixmap)
        self.labelImageDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.labelImageDisplay.setScaledContents(True)
        self.labelImageDisplay.setMinimumSize(1, 1)
        self.labelImageDisplay.show()

    def handleClick(self):
        self.viewIconClicked(self.name, self.pixmap)

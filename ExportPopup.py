from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import csv


class ExportPopup(QWidget):
    def __init__(self, vectorName, vectorTableWidget, relationshipTableWidget, figure):
        super(ExportPopup, self).__init__()
        self.vectorName = vectorName
        self.vectorTableWidget = vectorTableWidget
        self.relationshipTableWidget = relationshipTableWidget
        self.figure = figure
        self.layout = QVBoxLayout()
        self.locationLabel = QLabel()
        self.locationLabel.setText("Location: ")
        self.locationLabel.setFont(QtGui.QFont('SansSerif', 7))
        self.layout.addWidget(self.locationLabel)
        self.fileDialog = QFileDialog()
        self.fileDialog.setFileMode(QFileDialog.AnyFile)
        self.layout.addWidget(self.fileDialog)
        self.exportButton = QPushButton('Export', self)
        self.exportButton.setFont(QtGui.QFont('SansSerif', 7))
        self.exportButton.clicked.connect(self.onExportClick)
        self.layout.addWidget(self.exportButton)
        self.setLayout(self.layout)
        self.setWindowTitle("Export Popup")

    def exportVectorTable(self, exportPath):
        filename = exportPath + "/" + self.vectorName + "_SignificantEventTable.csv"
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=",", lineterminator='\n')
            model = self.vectorTableWidget.model()
            row = list()
            row.append("ID")
            for col_num in range(model.columnCount()):
                row.append(model.headerData(col_num, QtCore.Qt.Horizontal))
            writer.writerow(row)
            for row_num in range(model.rowCount()):
                row = list()
                row.append(str(model.headerData(row_num, QtCore.Qt.Vertical)))
                for col_num in range(model.columnCount()):
                    text = model.data(model.index(row_num, col_num))
                    row.append(str(text))
                writer.writerow(row)

    def exportRelationshipTable(self, exportPath):
        filename = exportPath + "/" + self.vectorName + "_RelationshipTable.csv"
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=",", lineterminator='\n')
            model = self.relationshipTableWidget.model()
            row = list()
            row.append("ID")
            for col_num in range(model.columnCount()):
                row.append(model.headerData(col_num, QtCore.Qt.Horizontal))
            writer.writerow(row)
            for row_num in range(model.rowCount()):
                row = list()
                row.append(str(model.headerData(row_num, QtCore.Qt.Vertical)))
                for col_num in range(model.columnCount()):
                    text = model.data(model.index(row_num, col_num))
                    row.append(str(text))
                writer.writerow(row)

    def exportGraph(self, exportPath):
        self.figure.savefig((exportPath + "/" + self.vectorName + "_Graph.png"), format="PNG")

    def onExportClick(self):
        exportPath = self.fileDialog.selectedFiles()[0]
        if len(exportPath) == 0:
            print("No export path selected.")
            return
        self.exportVectorTable(exportPath)
        self.exportRelationshipTable(exportPath)
        self.exportGraph(exportPath)
        self.close()

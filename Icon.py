from PyQt5 import QtGui
import matplotlib.image as mpimg

class Icon:

    DEFAULT = "Default"
    CUSTOM = "Custom"
    def __init__(self):
        self.name = ""
        self.source = ""
        self.rowIndexInTable = -1
        self.pixmap = None
        self.graphImage = None

    def getPixmapFromSource(self):
        self.pixmap = QtGui.QPixmap(self.source)

    def getGraphImageFromSource(self):
        self.graphImage = mpimg.imread(self.source)
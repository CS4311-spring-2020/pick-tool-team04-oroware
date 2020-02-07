from PyQt5 import QtGui
from imageio import imread

class Icon:

    DEFAULT = "Default"
    def __init__(self):
        self.name = ""
        self.source = ""
        self.rowIndexInTable = -1
        self.pixmap = None

    def getPixmapFromSource(self):
        self.pixmap = QtGui.QPixmap(self.source)
import pickle

from PyQt5 import QtGui, QtCore
import matplotlib.image as mpimg
import numpy as np
from PyQt5.QtCore import QDataStream, QIODevice, QByteArray
from PyQt5.QtGui import QPixmap


class Icon:

    DEFAULT = "Default"
    CUSTOM = "Custom"
    def __init__(self):
        self.name = ""
        self.source = ""
        self.rowIndexInTable = -1
        self.pixmapByteArray = None
        self.graphImage = None

    def getPixmapFromSource(self):
        pixmap = QtGui.QPixmap(self.source)
        self.pixmapByteArray = QByteArray()
        stream = QDataStream(self.pixmapByteArray, QIODevice.WriteOnly)
        stream << pixmap

    def getGraphImageFromSource(self):
        self.graphImage = mpimg.imread(self.source)

    def equals(self, icon):
        if self.name != icon.name:
            return False
        if self.source != icon.source:
            return False
        return True

class StoreQPixmap:
    def __init__(self):
        self._qpixmap = None

    def set_qpixmap(self, qpixmap):
        self._qpixmap = qpixmap

    def get_qpixmap(self):
        return self._qpixmap

    def __getstate__(self):
        state = QByteArray()
        stream = QDataStream(state, QIODevice.WriteOnly)
        stream << self._qpixmap
        return state

    def __setstate__(self, state):
        qpixmap = QPixmap()
        stream = QDataStream(state, QIODevice.ReadOnly)
        stream >> qpixmap
        self._qpixmap = qpixmap
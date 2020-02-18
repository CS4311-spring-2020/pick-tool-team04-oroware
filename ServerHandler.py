from IconManager import IconManager
from LogEntryManager import LogEntryManager
from VectorManager import VectorManager


class ServerHandler():
    def __init__(self):
        self.logEntryManager = LogEntryManager()
        self.vectorManager = VectorManager()
        self.iconManager = IconManager()
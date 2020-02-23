from Icon import Icon

class SignificantEvent:
    def __init__(self):
        self.id = None
        self.logEntry = None
        self.name = ""
        self.iconType = Icon.DEFAULT
        self.icon = None
        self.description = ""
        self.position = None
        self.rowIndexInTable = -1
        self.visible = True

    def equals(self, significantEvent):
        if self.id != significantEvent.id:
            return False
        if self.name != significantEvent.name:
            return False
        if self.description != significantEvent.description:
            return False
        if self.position != significantEvent.position:
            return False
        if self.visible != significantEvent.visible:
            return False
        if self.iconType != significantEvent.iconType:
            return False
        if self.icon == None and significantEvent.icon == None:
            return True
        if self.icon != None and significantEvent.icon != None:
            if not self.icon.equals(significantEvent.icon):
                return False
        else:
            return False
        return True
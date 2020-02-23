class Relationship:
    def __init__(self):
        self.id = None
        self.sourceSignificantEventId = None
        self.destSignificantEventId = None
        self.description = ""
        self.rowIndexInTable = -1

    def equals(self, relationship):
        if self.id != relationship.id:
            return False
        if self.description != relationship.description:
            return False
        if self.sourceSignificantEventId != relationship.sourceSignificantEventId:
            return False
        if self.destSignificantEventId != relationship.destSignificantEventId:
            return False
        return True
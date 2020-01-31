from Relationship import Relationship
from SignifcantEvent import SignificantEvent

class Vector:
    def __init__(self):
        self.vectorName = ""
        self.vectorDescription = ""
        self.vectorDimensions = 5
        self.significantEvents = dict()
        self.relationships = dict()

    def addSignificantEventFromLogEntry(self, logEntry):
        if not self.isLogEntryEventInVector(logEntry.id):
            event = SignificantEvent()
            event.logEntry = logEntry
            if len(self.significantEvents) == 0:
                event.id = 0
                event.position = (event.id, 1)
            elif (max(list(self.significantEvents.keys())) + 1) < self.vectorDimensions:
                event.id = max(list(self.significantEvents.keys())) + 1
                event.position = (event.id, 1)
            else:
                event.id = max(list(self.significantEvents.keys())) + 1
                event.position = (self.vectorDimensions, 1)
            self.significantEvents[event.id] = event

    def removeSignificantEvent(self, eventId):
        del self.significantEvents[eventId]
        deadRelationships = list()
        for relationshipId, relationship in self.relationships.items():
            if relationship.sourceSignificantEventId == eventId or relationship.destSignificantEventId == eventId:
                deadRelationships.append(relationshipId)
        for relationshipId in deadRelationships:
            del self.relationships[relationshipId]

    def removeSignificantEventByLogEntryId(self, logEntryId):
        significantEventId = -1
        for _, significantEvent in self.significantEvents.items():
            if significantEvent.logEntry.id == logEntryId:
                significantEventId = significantEvent.id
        if significantEventId != -1:
            self.removeSignificantEvent(significantEventId)

    def isLogEntryEventInVector(self, logEntryId):
        for _, significantEvent in self.significantEvents.items():
            if significantEvent.logEntry.id == logEntryId:
                return True
        return False

    def updateLogEntry(self, logEntry):
        for _, significantEvent in self.significantEvents.items():
            if significantEvent.logEntry.id == logEntry.id:
                significantEvent.logEntry.description = logEntry.description

    def addNewRelationship(self, sourceId, destId):
        relationship = Relationship()
        relationship.sourceSignificantEventId = sourceId
        relationship.destSignificantEventId = destId
        relationship.id = 0 if len(self.relationships) == 0 else (max(list(self.relationships.keys())) + 1)
        self.relationships[relationship.id] = relationship

    def removeRelationship(self, relationshipId):
        del self.relationships[relationshipId]

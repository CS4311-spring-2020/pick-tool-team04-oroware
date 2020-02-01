from PyQt5.QtWidgets import *

class RelationshipPopup(QWidget):
    def __init__(self, vector, relationship, trigger):
        super(RelationshipPopup, self).__init__()
        self.vector = vector
        self.relationship = relationship
        self.trigger = trigger
        self.trigger.connectVectorGraphTrigger()
        self.trigger.connectRelationshipTableTrigger()
        self.trigger.connectRelationshipTableEntryTrigger(self.relationship, self.vector.vectorName)
        layout = QVBoxLayout()
        self.relationshipDescriptionLabel = QLabel()
        self.relationshipDescriptionLabel.setText("Label:")
        layout.addWidget(self.relationshipDescriptionLabel)
        self.relationshipDescriptionTextEdit = QPlainTextEdit()
        self.relationshipDescriptionTextEdit.setPlainText(self.relationship.description)
        layout.addWidget(self.relationshipDescriptionTextEdit)
        self.sourceIdLabel = QLabel()
        self.sourceIdLabel.setText("Source Event ID: " + str(self.relationship.sourceSignificantEventId))
        layout.addWidget(self.sourceIdLabel)
        self.destinationIdLabel = QLabel()
        self.destinationIdLabel.setText("Destination Event ID: " + str(self.relationship.destSignificantEventId))
        layout.addWidget(self.destinationIdLabel)
        self.deleteButtonRelationshipPopup = QPushButton('Delete', self)
        self.deleteButtonRelationshipPopup.clicked.connect(self.delete)
        layout.addWidget(self.deleteButtonRelationshipPopup)
        self.saveButtonRelationshipPopup = QPushButton('Save Changes', self)
        self.saveButtonRelationshipPopup.clicked.connect(self.onSaveClick)
        layout.addWidget(self.saveButtonRelationshipPopup)
        self.setLayout(layout)
        self.setWindowTitle("Relationship Edit Popup")

    def onSaveClick(self):
        self.relationship.description = self.relationshipDescriptionTextEdit.toPlainText()
        self.trigger.emitRelationshipTableEntryTrigger()
        self.close()

    def delete(self):
        self.vector.removeRelationship(self.relationship.id)
        self.trigger.emitRelationshipTableTrigger()
        self.trigger.emitVectorGraphTrigger()
        self.close()


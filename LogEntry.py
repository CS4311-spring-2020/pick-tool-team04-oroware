class LogEntry:
    WHITE_TEAM = "White Team"
    BLUE_TEAM = "Blue Team"
    RED_TEAM = "Red Team"

    def __init__(self):
        self.date = ""
        self.creator = ""
        self.description = ""
        self.artifact = ""
        self.id = ""
        self.associatedVectors = list()
from Vector import Vector

class VectorManager:
    def __init__(self):
        self.vectors = dict()
        sampleVector = Vector()
        sampleVector.vectorName = "SQL Attack"
        self.vectors[sampleVector.vectorName] = sampleVector
class RoundRobin:
    
    def __init__(self, avaiablePositions):
        self.list = []
        self.avaiablePositions =avaiablePositions
        self.startTime = None
        self.endTime = None

    def avaiable(self):
        if self.avaiablePositions != 0:
            return True
        else:
            return False
    
    def add(self, segment):
        self.list.append(segment)
        self.avaiablePositions -= 1

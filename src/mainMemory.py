from queue import Queue

class MainMemory:
    
    def __init__(self, size, relocationTime):
        self.avaiableSpace = size
        self.relocationTime = relocationTime
        self.queue = Queue()
        self.alocatedSegments = []

    def request(self, segment):

        if(self.avaiableSpace > segment.size):
            self.alocatedSegments.append(segment)
            self.avaiableSpace -= segment.size
            return True
        else:
            self.queue.enqueue(segment)
            return False
    
    def release(self, segment):

        # verificar se segmento existe
        self.alocatedSegments.remove(segment)
        self.avaiableSpace += segment.size

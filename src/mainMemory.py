from myQueue import Queue

class MainMemory:
    
    def __init__(self, size, relocationTime):
        self.avaiableSpace = size
        self.relocationTime = relocationTime
        self.queue = Queue()
        self.alocatedSegments = []

    def request(self, job):
        # request de memoria somento apos arrival
        for segment in job.segmentMapTable:
            if(self.avaiableSpace > segment.size):
                self.alocatedSegments.append(segment)
                self.avaiableSpace -= segment.size
                segment.alocated = True

        hasNotAlocatedSeg = False

        for segment in job.segmentMapTable:
            if not segment.alocated:
                hasNotAlocatedSeg = True
        
        if(hasNotAlocatedSeg):
            self.queue.enqueue(job)
    
    def release(self, segment):
        
        # release por segmento
        self.alocatedSegments.pop(0)
        self.avaiableSpace += segment.size
        segment.alocated = False

        # analisa primeiro job da fila
        if len(self.queue.queue) > 0:
            for segment in self.queue.queue[0].segmentMapTable:
                if (not segment.alocated) and (not segment.done):
                    if(self.avaiableSpace > segment.size):
                        self.alocatedSegments.append(segment)
                        self.avaiableSpace -= segment.size
                        segment.alocated = True

            # tira da fila se nao tiver mais segmentos nao alocados
            dequeue = True

            for segment in self.queue.queue[0].segmentMapTable:
                if not segment.alocated:
                    if not segment.done:
                        dequeue = False
            
            if(dequeue):
                self.queue.dequeue

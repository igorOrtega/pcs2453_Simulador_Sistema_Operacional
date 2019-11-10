from queue import Queue

class MainMemory:
    
    def __init__(self, size, relocationTime):
        self.avaiableSpace = size
        self.relocationTime = relocationTime
        self.queue = Queue()
        self.alocatedSegments = []

    def request(self, job):
        # request por Job
        for segment in job.segmentMapTable:
            # so aloca segmentos que nao estao alocados e nao terminaram o processamento
            if (not segment.alocated) and (not segment.processed):
                if(self.avaiableSpace > segment.size):
                    self.alocatedSegments.append(segment)
                    self.avaiableSpace -= segment.size

                    segment.alocated = True

        try:
            next(segment for segment in job.segmentMapTable if not segment.alocated)
            # fila de segmentos
            self.queue.enqueue(job)
        except:
            # nao existe nenhum segmento para se alocar
            pass
    
    def release(self, segment):
        
        # release por segmento
        self.alocatedSegments.remove(segment)
        self.avaiableSpace += segment.size

        # analisa primeiro job da fila

        for segment in self.queue[0].segmentMapTable:
            if (not segment.alocated) and (not segment.processed):
                if(self.avaiableSpace > segment.size):
                    self.alocatedSegments.append(segment)
                    self.avaiableSpace -= segment.size

                    segment.alocated = True

        try:
            # mantem na fila
            next(segment for segment in self.queue[0].segmentMapTable if not segment.alocated)
        except:
            self.queue.dequeue()

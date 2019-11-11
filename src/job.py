class Job:
    
    # inicializado na maix (leitura de disco)
    def __init__(self, name, segmentMapTable):
        self.name = name
        self.segmentMapTable = segmentMapTable

    def __str__(self):
        srtJob = "Name: %s \n"%(self.name)
        srtJob += "    Segments: \n"
        for segment in self.segmentMapTable:
            srtJob += "        id: %s"%(str(segment.id))
            srtJob +=", size: %s"%(str(segment.size))
            srtJob +=", alocated: %s"%(str(segment.alocated))
            srtJob +=", processing: %s"%(str(segment.processing))
            srtJob +=", time to finish: %s"%(str(segment.timeToProcess))
            srtJob +=", done: %s"%(str(segment.done))
            srtJob +=", has pend IO: %s\n"%(str(segment.hasIoOp()))

        return srtJob
    
class Job:
    
    # inicializado na maix (leitura de disco)
    def __init__(self, name, time, segmentMapTable):
        self.name = name
        self.executionTime = time
        self.segmentMapTable = segmentMapTable
    
    #def __str__(self):
     #   return "[%s, %s, %s]"%(self.name, self.executionTime, self.executionTime)
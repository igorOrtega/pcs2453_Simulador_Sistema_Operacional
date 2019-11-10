class Job:
    
    # inicializado na maix (leitura de disco)
    def __init__(self, name, segmentMapTable):
        self.name = name
        self.segmentMapTable = segmentMapTable
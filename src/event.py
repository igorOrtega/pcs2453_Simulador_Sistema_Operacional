class Event:
    
    def __init__(self, eJob, eTime, eType):
        self.job = eJob
        self.time = eTime
        self.type = eType

    def __str__(self):
        strEvent = "Instante de ocorrencia: %s, Tipo: %s, Job Associado: %s"%(str(self.time), self.type, self.job.name)
        return strEvent
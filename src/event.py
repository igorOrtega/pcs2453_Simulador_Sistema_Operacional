from job import Job

class Event:
    
    def __init__(self, eJob, eTime, eType):
        self.job = eJob
        self.time = eTime
        self.type = eType

    def __str__(self):
        if type(self.job) is Job:
            jobName = self.job.name
        else:
            jobName = ""
        strEvent = "Instante de ocorrencia: %s, Tipo: %s, Job Associado: %s"%(str(self.time), self.type, jobName)
        return strEvent
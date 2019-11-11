from job import Job
from segment import Segment
from ioOp import IoOp

class Disk:

    def __init__(self, arquivo):

        self.avaiablesJobs = []

        f = open(arquivo, "r")

        lines = f.readlines()
        
        jobName = None
        segMapTable = []
        segmentInfo = None
        ioOp = []

        for line in lines:
            # remove pula de linha
            line = line[:-1]
            # linhas que comecam com "#" sao comentarios
            if not line.startswith("#"):
                # --- se for job id
                if line.startswith("Job"):
                    # pega valores lidos    
                    jobName = line.split(":")[1]

                # se e um definicao de segmento
                elif line.startswith("Segment"):
                    if not segmentInfo == None:
                        newSeg = Segment(segmentInfo[0], int(segmentInfo[1]), int(segmentInfo[2]), ioOp)
                        segMapTable.append(newSeg)
                        ioOp = []
                # pega valores lidos
                    segmentInfo = line.split(":", 1)[1]
                    segmentInfo = segmentInfo.split(",")
                # 
                elif line.startswith("IoOp"):
                    ioInfo =  line.split(":")[1]
                    ioInfo = ioInfo.split(",")
                    newIoOp = IoOp(ioInfo[0], ioInfo[1], ioInfo[2])

                    ioOp.append(newIoOp)
                
                elif line == "endJob":
                    # salva ultimo segmento
                    newSeg = Segment(segmentInfo[0], int(segmentInfo[1]), int(segmentInfo[2]), ioOp)
                    segMapTable.append(newSeg)
                    segmentInfo = None
                    ioOp = []
                    # salva Job
                    newJob = Job(jobName, segMapTable)
                    self.avaiablesJobs.append(newJob)
                    segMapTable = []


                    




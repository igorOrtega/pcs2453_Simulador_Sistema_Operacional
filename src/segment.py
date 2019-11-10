from ioOp import IoOp

class Segment:

    def __init__(self, id, size, timeToProcess, ioOperationsList):
        self.id = id
        self.size = size
        self.timeToProcess = timeToProcess
        self.ioOperationsList = ioOperationsList
        self.alocated = False
        self.processed = False

    def decreaseTime(self, valor):
        if(valor > self.timeToProcess):
            self.timeToProcess = 0
        else:
            self.timeToProcess -= valor

    def hasIoOp(self):

        pending = False
        for ioOp in self.ioOperationsList:
            if (ioOp.finished == False):
                pending = True
        
        return pending
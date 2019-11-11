from ioOp import IoOp

class Segment:

    def __init__(self, id, size, timeToProcess, ioOperationsList):
        self.id = id
        self.size = size
        self.timeToProcess = timeToProcess
        self.ioOperationsList = ioOperationsList
        self.alocated = False
        self.processing = False
        self.done = False

    def decreaseTime(self, valor):
        if(valor >= self.timeToProcess):
            self.timeToProcess = 0
            self.done = True
        else:
            self.timeToProcess -= valor

    def hasIoOp(self):

        pending = False
        for ioOp in self.ioOperationsList:
            if (ioOp.finished == False):
                pending = True
        
        return pending
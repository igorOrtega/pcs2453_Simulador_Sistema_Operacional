from ioOp import IoOp

class Segment:

    def __init__(self, size, arraivalTime, timeToProcess, ioOperationsList):
        self.size = size
        self.arraivalTime = arraivalTime
        self.timeToProcess = timeToProcess
        self.ioOperationsList = ioOperationsList

    def decreaseTime(self, valor);
        if(valor > self.timeToProcess):
            self.timeToProcess = 0
        else:
            self.timeToProcess -= valor

    def hasIoOp(self):

        pending = False
        for ioOp in ioOperationsList:
            if ioOp.finished = false
                pending = True
        
        return pending
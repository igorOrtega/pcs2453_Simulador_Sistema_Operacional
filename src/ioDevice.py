from myQueue import Queue

class IoDevice:

    def __init__(self, dType, timePerOp):
        self.type = dType
        self.timePerOp = timePerOp
        self.queue = Queue()
        self.busy = False

    def request(self, ioOp):
        # se estiver livre retorna True, se nao coloca na fila e retorna false
        if (self.busy != True):
            self.busy = True
            ioOp.processing = True
            return True
        else:
            self.queue.enqueue(ioOp)
            return False

    # retorna true se tiver pendencias na fila
    def release(self, ioOp):

        self.busy = False
        ioOp.processing = False
        ioOp.finished = True

        addedIo = None

        if len(self.queue.queue) > 0:
            addedIo = self.queue.dequeue()

        return addedIo

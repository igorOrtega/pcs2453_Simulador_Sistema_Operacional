from myQueue import Queue

class IoDevice:

    def __init__(self, dType, timePerOp):
        self.type = dType
        self.timePerOp = timePerOp
        self.queue = Queue()
        self.busy = False

    def request(self, segment):
        # se estiver livre retorna True, se nao coloca na fila e retorna false
        if (self.busy != True):
            return True
        else:
            self.queue.enqueue(segment)
            return False

    # retorna true se tiver pendencias na fila
    def release(self):

        self.busy = False

        if len(self.queue) != 0:
            self.queue.dequeue
            return True
        else:
            return False
        
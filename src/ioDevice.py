from queue import Queue

class IoDevice:

    def __init__(self, dType, timePerOp):
        self.type = dType
        self.timePerOp = timePerOp
        self.queue = Queue()
        self.busy = False

    def request(self, segment):

        if !(self.busy):
            self.busy = True
            return True
        else:
            self.queue.enqueue(segment)
            return False

    def release(self):

        self.busy = False

        if len(queue) != 0:
            queue.dequeue
        
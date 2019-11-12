class IoOp:

    def __init__(self, id, device, numberOfRepeticions) :
        self.id = id
        self.device = device
        self.numberOfRepeticions = numberOfRepeticions
        self.processing = False
        self.finished = False
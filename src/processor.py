
from queue import Queue
from roundRobin import RoundRobin

class Processor:
    
    # Atributos: queue, cpuSliceTime, roundRobin

    def __init__(self, sliceTime):
        self.sliceTime = sliceTime
        self.queue = Queue()
        self.roundRobin = RoundRobin(5)
    
    # metodos: request, release, isBusy

    # tenta adicionar segmento ao Round Robin, se nao conseguir coloca na queue. 
    def request(self, segment, time):

        # se nao ha posicoes disponiveis
        if(not self.roundRobin.avaiable()):
            # coloca na fila
            self.queue.enqueue(segment)
        # se processador ja comecou a processar algo (tempo de inicio round robin diferente do tempo do segmento)
        elif(self.roundRobin.startTime != time and self.roundRobin.startTime != None):
            # coloca na fila
            self.queue.enqueue(segment)
        # Se passou por tudo, pode colocar no Round Robin
        else:
            self.roundRobin.add(segment)
            self.roundRobin.startTime = time
            self.roundRobin.endTime = time + self.sliceTime
    
    def run(self, segment):
        # se tiver no Round Robin atualiza tempo para processar
        isOnRoundRabin = False

        for seg in self.roundRobin.list:
            if seg.id == segment.id:
                isOnRoundRabin = True
                break
        
        if(isOnRoundRabin):
            segment.decreaseTime(self.sliceTime)


    def release(self, segment):
        # verificar se segmento existe
        self.roundRobin.list.remove(segment)
        self.roundRobin.avaiablePositions += 1



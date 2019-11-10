
from queue import Queue
from roundRobin import RoundRobin

class Processor:
    
    # Atributos: queue, cpuSliceTime, roundRobin

    def __init__(self, cpuSliceTime):
        self.cpuSliceTime = cpuSliceTime
        self.queue = Queue()
        self.roundRobin = RoundRobin(5)
    
    # métodos: request, release, isBusy

    # tenta adicionar segmento ao Round Robin, se não conseguir coloca na queue. 
    def request(self, segment, time):

        # se não há posicoes disponiveis
        if(self.roundRobin.avaiablePositions == 0):
            # coloca na fila
            self.queue.enqueue(segment)
            return False
        # se processador já comecou a processar algo (tempo de inicio round robin diferente do tempo do segmento)
        elif(self.roundRobin.startTime != time and self.roundRobin.startTime != None):
            # coloca na fila
            self.queue.enqueue(segment)
            return False
        # Se passou por tudo, pode colocar no Round Robin
        else:
            self.roundRobin.list.append(segment)
            self.roundRobin.avaiablePositions -= 1
            self.roundRobin.startTime = time

            return True
    
    def release(self, segment, time):
        # verificar se segmento existe
        self.roundRobin.list.remove(segment)
        self.roundRobin.avaiablePositions += 1

        # Se todos os segmentos que foram processados sairam do Round Robin, reseta o tempo e pega segmentos da fila
        if(len(self.roundRobin.list) == 0):
            self.roundRobin.startTime = None

            while (self.roundRobin.avaiablePositions != 0 and len(self.queue) != 0):
                nextSegment = self.queue.dequeue()
                self.roundRobin.list.append(nextSegment)
                self.roundRobin.avaiablePositions -= 1
                self.roundRobin.startTime = time

        return True

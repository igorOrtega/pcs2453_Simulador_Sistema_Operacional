from disk import Disk
from event import Event
from ioDevice import IoDevice
from ioOp import IoOp
from job import Job
from mainMemory import MainMemory
from processor import Processor
from myQueue import Queue
from roundRobin import RoundRobin
from segment import Segment
from eventList import EventList

import os
import time

class Simulator:
    
    def __init__(self, simulationTotalTime):
        self.simulationEndTime = simulationTotalTime
        self.currentInstant = 0
        self.eventList = EventList()
        self.simulatedJobs = []

        # inicia com log ativo
        self.log = True

        # inicializa principais componentes
        self.cpu = Processor(10) #10 unidades de tempo para slice time
        self.memory = MainMemory(256, 20) # tamanho: 256 bytes, tempo de relocacao: 100 unidade de tempo
        self.disk = Disk("disk.txt") # disco possui jobs disponiveis a serem disputados

        self.devices = {
            "printer1" : IoDevice("printer1", 1),
            "printer2" : IoDevice("printer2", 5),
            "scanner1" : IoDevice("scanner1", 5),
            "scanner2" : IoDevice("scanner2", 10)
        }


    # loop principal do simulador
    def main(self):

        # tela para programar simulacao (escolha de jobs e tempos)

        choose = 1

        # loop escolhas de jobs no disco
        while(choose != 0):
            # limpa tela
            os.system('cls' if os.name == 'nt' else 'clear')

            print("Simulador Sistema Operacional - PCS2453\n")

            print("Escolha os Jobs a serem executados, e seus respctivos tempos: \n")

            print("Jobs: \n")
            i = 0
            for job in self.disk.avaiablesJobs:
                i += 1
                print("%s - "%(i) + job.name)
            print("\n")
            jobChoose = input("Escreva o nome de um: ")
            jobArrivalTime = int(input("Tempo de chegada no simulador: "))

            found = False
            
            for job in self.disk.avaiablesJobs:
                if job.name == jobChoose:
                    found = True
                    selectedJob = job
                    break
            
            # se achou continua
            if found:
                # adiciona job a lista de jobs simulados
                self.simulatedJobs.append(selectedJob)

                # cria evento
                newEvent = Event(selectedJob, jobArrivalTime, "JOB ARRIVAL")

                # adiciona a lista de eventos
                self.eventList.add(newEvent)

            else:
                print("\n")
                print("Job inexistente no disco!")

            print("\n")
            print("Deseja continuar selecionando Jobs para simular? ")
            choose = int(input("1 - Sim, 0 - Nao\n"))


        while(self.simulationEndTime > self.currentInstant and choose != "5"):
            # limpa tela
            os.system('cls' if os.name == 'nt' else 'clear')

            print("Simulador Sistema Operacional - PCS2453\n")

            print("1 - Enable Log, 2 - Disable Log, 3 - Alter Simulation End Time, ENTER - Run One Time Unit\n")
            
            choose = input()
            # enable log
            if choose == "1":
                if self.log:
                    print("Log ja ativado")
                    time.sleep(1)
                else:
                    self.eventList.add(Event(None, self.currentInstant, "ENABLE LOG"))
            # disable log
            elif choose == "2":
                if not self.log:
                    print("Log ja desativado")
                    time.sleep(1)
                else:
                    self.eventList.add(Event(None, self.currentInstant, "DISABLE LOG"))
            # alter simulation end time
            elif choose == "3":
                valor = int(input("\nEscolha novo final para simulacao: "))
                self.eventList.add(Event(valor, self.currentInstant, "ALTER SIMULATION END TIME"))
                
            # run events for the current instant
            elif choose == "":

                print("\n Simulating ... \n")
                
                if len(self.eventList.events) > 0:
                    hasEventToSim = (self.eventList.events[0].time == self.currentInstant)
                else:
                    hasEventToSim = False

                while(hasEventToSim and self.eventList.total != 0):

                    if (self.eventList.events[0].time == self.currentInstant):
                        # existe evento para tratar
                        currentEvent = self.eventList.pop()
                        eventType = currentEvent.type

                        
                        print("Current Event: " + str(currentEvent))
                        input()

                        # aciona rotinas de tratamento de acordo com o tipo de evento

                        if eventType == "JOB ARRIVAL":
                            #
                            self.arrival(currentEvent.job)

                        elif eventType == "REQUEST MEM":
                            #
                            self.reqMemory(currentEvent.job)

                        elif eventType == "RELEASE MEM":
                            #
                            self.releaseMemory(currentEvent.job)

                        elif eventType == "REQUEST CPU":
                            #
                            self.reqCpu(currentEvent.job)

                        elif eventType == "PROCESS CPU":
                            #
                            self.processCpu(currentEvent.job)

                        elif eventType == "RELEASE CPU":
                            #
                            self.releaseCpu(currentEvent.job)

                        elif eventType == "REQUEST IO":
                            #
                            self.reqIo(currentEvent.job)

                        elif eventType == "RELEASE IO":
                            #
                            self.releaseIo(currentEvent.job)

                        elif eventType == "ENABLE LOG":
                            #
                            self.enableLog()

                        elif eventType == "DISABLE LOG":
                            #
                            self.disableLog()

                        elif eventType == "ALTER SIMULATION END TIME":
                            #
                            self.alterSimulationEndTime(currentEvent.job)

                        # verifica se proximo evento da lista possui mesmo tempo de execucao
                        if len(self.eventList.events) > 0:
                            hasEventToSim = (self.eventList.events[0].time == self.currentInstant)
                        else:
                            hasEventToSim = False
                #atualiza tempo
                self.currentInstant += 1
                # limpa tela
                os.system('cls' if os.name == 'nt' else 'clear')

                print("Simulador Sistema Operacional - PCS2453\n")
                print("Tempo Atual: " + str(self.currentInstant) + "\n")
                input()

                # printa log atual
                if(self.log and (eventType != "ENABLE LOG" or eventType != "DISABLE LOG" or eventType != "ALTER SIMULATION END TIME")):

                    print("Jobs Simulados: \n")
                    
                    i = 0
                    
                    for j in self.simulatedJobs:
                        i += 1
                        print("job %s: "%(str(i)))
                        print(j)

                    print("Event List: \n")
                    i = 0
                    for e in self.eventList.events:
                        i += 1
                        print(str(i) + " - " + str(e))
                    
                    print("\nComputer Infos: \n")

                    print("Processor: ")
                    print("Round Robin Start Time: " + str(self.cpu.roundRobin.startTime))
                    print("Round Robin End Time: " + str(self.cpu.roundRobin.endTime))
                    print("Avaiable position: " + str(self.cpu.roundRobin.avaiablePositions))
                    print("\nMemory: ")
                    print("avaible space (bytes): " + str(self.memory.avaiableSpace))
                    print("\nDevice Status: ")
                    # Printer 1
                    if (self.devices["printer1"].busy):
                        infoP1 = "busy"
                    else:
                        infoP1 = "free"
                    print("printer 1: " + infoP1)
                    # Printer 2
                    if (self.devices["printer2"].busy):
                        infoP2 = "busy"
                    else:
                        infoP2 = "free"
                    print("printer 2: " + infoP2)
                    # Scanner 1
                    if (self.devices["scanner1"].busy):
                        infoS1 = "busy"
                    else:
                        infoS1 = "free"
                    print("Scanner 1: " + infoS1)
                    # Scanner 1
                    if (self.devices["scanner2"].busy):
                        infoS2 = "busy"
                    else:
                        infoS2 = "free"
                    print("Scanner 2: " + infoS2)

                    
                    input()

            else:
                print("Escolha inválida")


        print("SIMULACAO FINALIZADA!!")
        time.sleep(2)

    
    # tratamentos de eventos

    def arrival(self, job):
        # cria evento de para solicitar memoria
        self.eventList.add(Event(job, self.currentInstant, "REQUEST MEM"))

    def reqMemory(self, job):
        # solicita uso da memoria
        self.memory.request(job)

        try:
           # existem segmentos alocados = > cria evento
            next(segment for segment in job.segmentMapTable if segment.alocated)
            self.eventList.add(Event(job, self.currentInstant + self.memory.relocationTime, "REQUEST CPU"))
        except:
            # se não conseguiu alocar nada, nao cria evento
            pass

    def releaseMemory(self, job):

        pendToProc = []

        # libera memoria ocupado por segmento "done"
        for segment in job.segmentMapTable:
            if (segment.done and segment.alocated):
                pendToProc += self.memory.release(segment)
                
        

        # descobre a quais jobs os segmentos adicionados pertencem e cria evento process para tais
        

        createReqEvent = []
        for segment in pendToProc:
            for job in self.simulatedJobs:
                if segment in job.segmentMapTable:
                    createReqEvent.append(job)
        
        for job in createReqEvent:
            self.eventList.add(Event(job, self.currentInstant + self.memory.relocationTime, "REQUEST CPU"))

    def reqCpu(self, job):
        #

        addedSeg = []
        for segment in job.segmentMapTable:
            if (segment.alocated and not segment.processing):
                self.cpu.request(segment, self.currentInstant)
                # A partir do momento em que vai para o processador vira "processing"
                segment.processing = True
                addedSeg.append(segment)


        createEvent = False
        for seg in addedSeg:
            if seg in self.cpu.roundRobin.list:
                createEvent = True

        if createEvent:
            self.eventList.add(Event(job, self.currentInstant + self.cpu.sliceTime, "PROCESS CPU"))


    def processCpu(self, job):
        # run nos segmentos not dones
        for segment in job.segmentMapTable:
            if(not segment.done and segment.processing):
                self.cpu.run(segment)
        
        # apos run faz analises para definir eventos criados (existe a possibilidade de um mesmo job possuir eventos de release e process cpu)
        createRelease = False
        createProcess = False
        for segment in job.segmentMapTable:
            if segment.done and segment.processing:
                createRelease = True
            # se nao esta pronto, analisa se tem IO
            elif segment.alocated and segment.processing:
                if segment.hasIoOp():
                    createRelease = True
                else:
                    createProcess = True
        
        #cria eventos
        if createRelease:
            self.eventList.add(Event(job, self.currentInstant, "RELEASE CPU"))
        if createProcess:
            self.eventList.add(Event(job, self.currentInstant + self.cpu.sliceTime, "PROCESS CPU"))
            self.cpu.roundRobin.startTime = self.currentInstant
            self.cpu.roundRobin.endTime = self.currentInstant + self.cpu.sliceTime
            
    def releaseCpu(self, job):

        # processing done:
        #   has Io? y => release, req Io, n => release, release mem
        # 
        # processing hasIO y => release, req IO, n => nothing to do  

        createIo = False
        createReleaseMem = False

        for segment in job.segmentMapTable:
            if segment.processing and segment.done:
                self.cpu.release(segment)
                segment.processing = False
                if (segment.hasIoOp()):
                    createIo = True
                else:
                    createReleaseMem = True
            # not finished, mas analisa IO
            elif segment.processing:
                if segment.hasIoOp():
                    self.cpu.release(segment)
                    segment.processing = False
                    createIo = True

        # reseta tempo de inicio round robin
        self.cpu.roundRobin.startTime = None

        #cria eventos
        if createIo:
            self.eventList.add(Event(job, self.currentInstant, "REQUEST IO"))
        if createReleaseMem:
            self.eventList.add(Event(job, self.currentInstant, "RELEASE MEM"))
        
        # tenta colocar o maximo de segmentos da fila no roundRobin, se tiver algo na fila
        if len(self.cpu.queue.queue) > 0:

            addedSeg = []
            while(self.cpu.roundRobin.avaiable() and len(self.cpu.queue.queue) > 0):
                nextSegment = self.cpu.queue.dequeue()
                self.cpu.roundRobin.add(nextSegment)
                addedSeg.append(nextSegment)

            # reset timing round robin
            self.cpu.roundRobin.startTime = self.currentInstant
            self.cpu.roundRobin.endTime = self.currentInstant + self.cpu.sliceTime
            
            # descobre a quais jobs os segmentos adicionados pertencem e cria evento process para tais
            createProcEvent = []
            for segment in addedSeg:
                for job in self.simulatedJobs:
                    if segment in job.segmentMapTable:
                        createProcEvent.append(job)
            
            for job in createProcEvent:
                self.eventList.add(Event(job, self.currentInstant + self.cpu.sliceTime, "PROCESS CPU"))


    def reqIo(self, job):
        #
        for segment in job.segmentMapTable:
            if segment.hasIoOp():
                for io in segment.ioOperationsList:
                    if not io.finished:
                        opStart = self.devices[io.device].request(io)
                        if opStart:
                            ioTotalTime = io.numberOfRepeticions * self.devices[io.device].timePerOp
                            self.eventList.add(Event(job, self.currentInstant + ioTotalTime, "RELEASE IO"))
    
    def  releaseIo(self, job):
        # libera e pega ios da fila (já cria evento)
        addedIO = []
        for segment in job.segmentMapTable:
            if segment.hasIoOp():
                for io in segment.ioOperationsList:
                    if io.processing:
                        newIo = self.devices[io.device].release(io)
                        if newIo != None:
                            addedIO.append(newIo)
                           
                           
        # descobre de a quais jobs os ios adcionados pertencem
        if len(addedIO) > 0:
            for newIo in addedIO:
                for job in self.simulatedJobs:
                    for seg in job.segmentMapTable:
                        if (newIo in seg.ioOperationsList):
                            opStart = self.devices[newIo.device].request(newIo)
                            if opStart:
                                ioTotalTime = newIo.numberOfRepeticions * self.devices[io.device].timePerOp
                                self.eventList.add(Event(job, self.currentInstant + ioTotalTime, "RELEASE IO"))
            
        # analisa se job ja pode voltar para processador ou nao
        pend = False
        for segment in job.segmentMapTable:
            if segment.hasIoOp():
                pend = True

        if not pend:
             self.eventList.add(Event(job, self.currentInstant, "REQUEST CPU"))
    
    def enableLog(self):
        #
        self.log = True

    def disableLog(self):
        #
        self.log = False
    
    def alterSimulationEndTime(self, valor):
        #
        self.simulationEndTime = valor



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

        # inicializa principais componentes
        self.cpu = Processor(10) #10 unidades de tempo para slice time
        self.memory = MainMemory(256, 20) # tamanho: 256 bytes, tempo de relocacao: 100 unidade de tempo
        self.disk = Disk("disk.txt") # disco possui jobs disponiveis a serem disputados


    # loop principal do simulador
    def main(self):

        # tela para programar simulacao (escolha de jobs e tempos)

        choose = 1

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
            jobChoose = input("Escreve o nome de um: ")
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

            print("1 - Enable Log, 2 - Disable Log, 3 - Alter Simulation End Time, 4 - Run One Time Unit, 5 - Break Simulation \n")
            
            choose = int(input())
            # enable log
            if choose == 1:
                
                print("Escolha 1")
                time.sleep(1)
            # disable log
            elif choose == 2:
                print("Escolha 2")
                time.sleep(1)
            # alter simulation end time
            elif choose == 3:
                print("Escolha 3")
                time.sleep(1)
            # run events for the current instant
            elif choose == 4:
                
                hasEventToSim = (self.eventList.events[0].time == self.currentInstant)


                while(hasEventToSim and self.eventList.total != 0):

                    if (self.eventList.events[0].time == self.currentInstant):
                        # existe evento para tratar
                        currentEvent = self.eventList.pop()
                        eventType = currentEvent.type

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
                            self.alterSimulationEndTime()

                        # verifica se proximo evento da lista possui mesmo tempo de execucao
                        if len(self.eventList.events) > 0:
                            hasEventToSim = (self.eventList.events[0].time == self.currentInstant)
                        else:
                            hasEventToSim = False
                #atualiza tempo
                self.currentInstant += 1
                print("Tempo atual: " + str(self.currentInstant) + "\n")
                time.sleep(1)

           
            elif choose == 5:
                print("Escolha 5")
                time.sleep(1)
            else:
                print("Escolha inválida")
                time.sleep(1)

            

        # printa estatitiscas
        # limpa tela
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Simulador Sistema Operacional - PCS2453\n")

    
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

        # libera memoria ocupado por segmento "done"
        for segment in job.segmentMapTable:
            if (segment.done and segment.alocated):
                self.memory.release(segment)
                
        
        # analisa se tem job na fila
        if len(self.memory.queue.queue) > 0:
            try:
            # existem segmentos alocados e nao processados para o primeiro job da queue => cria evento
                next(segment for segment in self.memory.queue.queue[0] if segment.alocated and not segment.processing and not segment.done)
                self.eventList.add(Event(job, self.currentInstant + self.memory.relocationTime, "REQUEST CPU"))
            except:
                # se não conseguiu alocar nada, nao cria evento
                pass

    def reqCpu(self, job):
        #
        for segment in job.segmentMapTable:
            if (segment.alocated and not segment.processing):
                self.cpu.request(segment, self.currentInstant)
                # A partir do momento em que vai para o processador vira "processing"
                segment.processing = True

        try:
           # existem segmentos no round Robin => cria evento process para job, se nao espera liberar cpu
            next(segment for segment in job.segmentMapTable if segment in self.cpu.roundRobin.list)
            self.eventList.add(Event(job, self.currentInstant + self.cpu.sliceTime, "PROCESS CPU"))
        except:
            pass

    def processCpu(self, job):
        # run nos segmentos not dones
        for segment in job.segmentMapTable:
            if(not segment.done):
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

        #cria eventos
        if createIo:
            self.eventList.add(Event(job, self.currentInstant, "REQUEST IO"))
        if createReleaseMem:
            self.eventList.add(Event(job, self.currentInstant, "RELEASE MEM"))
        
        # tenta colocar o maximo de segmentos da fila no roundRobin, se tiver algo na fila
        if len(self.cpu.queue.queue) > 0:

            addedSeg = []
            while(self.cpu.roundRobin.avaiable()):
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
        return True
    
    def  releaseIo(self, job):
        #
        return True
    
    def enableLog(self):
        #
        return True

    def disableLog(self):
        #
        return True
    
    def alterSimulationEndTime(self):
        #
        return True


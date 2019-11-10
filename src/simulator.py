from disk import Disk
from event import Event
from ioDevice import IoDevice
from ioOp import IoOp
from job import Job
from mainMemory import MainMemory
from processor import Processor
from queue import Queue
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
        self.memory = MainMemory(256, 100) # tamanho: 256 bytes, tempo de relocacao: 100 unidade de tempo
        self.disk = Disk("disk.txt") # disco possui jobs disponiveis a serem disputados


    # loop principal do simulador
    def main(self):

        # tela para programar simulacao (escolha de jobs e tempos)

        choose = "1"

        while(choose != "0"):
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
            jobArrivalTime = input("Tempo de chegada no simulador: ")

            
            try:
                selectedJob = next(job for job in disk.avaiablesJobs if job.name == jobChoose)
                found = True
            except:
                found = False
            
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
            choose = input("1 - Sim, 0 - Nao\n")

        while(self.simulationEndTime > self.currentInstant and choose != "5"):
            # limpa tela
            os.system('cls' if os.name == 'nt' else 'clear')

            print("Simulador Sistema Operacional - PCS2453\n")

            print("1 - Enable Log, 2 - Disable Log, 3 - Alter Simulation End Time, 4 - Run One Time Unit, 5 - Break Simulation \n")
            
            choose = input()
            # enable log
            if choose == "1":
                
                print("Escolha 1")
                time.sleep(1)
            # disable log
            elif choose == "2":
                print("Escolha 2")
                time.sleep(1)
            # alter simulation end time
            elif choose == "3":
                print("Escolha 3")
                time.sleep(1)
            # run events for the current instant
            elif choose == "4":
                
                hasEventToSim = True

                while(hasEventToSim and self.eventList.total != 0):
                    
                    if (self.eventList[0].time == self.currentInstant):
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
                            self.releaseMemory()

                        elif eventType == "REQUEST CPU":
                            #
                            self.reqCpu()

                        elif eventType == "PROCESS CPU":
                            #
                            self.processCpu()

                        elif eventType == "RELEASE CPU":
                            #
                            self.releaseCpu()

                        elif eventType == "REQUEST IO":
                            #
                            self.reqIo()

                        elif eventType == "RELEASE IO":
                            #
                            self.releaseIo()

                        elif eventType == "ENABLE LOG":
                            #
                            self.enableLog()

                        elif eventType == "DISABLE LOG":
                            #
                            self.disableLog()

                        elif eventType == "ALTER SIMULATION END TIME":
                            #
                            self.alterSimulationEndTime()


                #atualiza tempo
                self.currentInstant += 1
            elif choose == "5":
                print("Escolha 5")
                time.sleep(1)
            else:
                print("Escolha inválida")
                time.sleep(1)

            

        # printa estatitiscas
        # limpa tela
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Simulador Sistema Operacional - PCS2453\n")
        input("Estatisicas")
    
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

    def releaseMemory(self):
        #
        return True

    def reqCpu(self):
        #
        return True

    def processCpu(self):
        #
        return True

    def releaseCpu(self):
        #
        return True
    
    def reqIo(self):
        #
        return True
    
    def  releaseIo(self):
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


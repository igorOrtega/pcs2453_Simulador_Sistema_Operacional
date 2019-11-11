class EventList:

    def __init__(self):
        self.events = []
        self.total = 0
    
    def add(self, event):
        # verifica se existe mesmo tipo de evento, para o mesmo tempo para o mesmo job na lista, se existir nao duplica
        
        eventNotExists = True

        for e in self.events:
            if e.type == event.type and e.time == event.time and e.job.name == event.job.name:
                eventNotExists = False

        if eventNotExists:                
            self.total += 1
            self.events.append(event)
            # ordena de acordo com tempo do evento
            self.events.sort(key = lambda event: event.time, reverse=False)
    
    def pop(self):
        self.total -= 1
        return self.events.pop(0)
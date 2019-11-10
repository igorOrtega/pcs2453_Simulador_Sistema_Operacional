class EventList:

    def __init__(self):
        self.events = []
        self.total = 0
    
    def add(self, event):
        
        self.total += 1
        self.events.append(event)
        # ordena de acordo com tempo do evento
        self.events.sort(key = lambda event: event.time, reverse=False)
    
    def pop(self):
        self.total -= 1
        return self.events.pop(0)
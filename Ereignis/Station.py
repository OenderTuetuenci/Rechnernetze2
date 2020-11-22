from Ereignis.Ereignisliste import Ereignisliste as eventList


class Station:
    def __init__(self, name, processingtime):
        self.name = name
        self.processing_time = processingtime
        self.queue = []

    def queueIn(self, customer):
        self.queue.append(customer)
        if len(self.queue) == 1:
            self.serve()

    def serve(self):
        if len(self.queue) <= 0:
            return
        kunde = self.queue.pop()
        time = eventList.simulationtime + self.processing_time * kunde.liste[0][2]
        eventList.push((time, 1, kunde.verlassen, []))

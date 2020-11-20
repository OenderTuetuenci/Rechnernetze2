from Ereignis.Ereignisliste import Ereignisliste as ev

class Station:
    def __init__(self,name,processingtime):
        self.name = name
        self.processingtime = processingtime
        self.queue = []
    def queueIn(self,kunde):
        self.queue.append(kunde)
        if len(self.queue) == 1:
            self.serve()
    def serve(self):
        if len(self.queue) <= 0:
            return
        kunde = self.queue.pop()
        time = ev.simulationszeit + self.processingtime * kunde.liste[0][2]
        ev.push((time,1,kunde.verlassen,[]))
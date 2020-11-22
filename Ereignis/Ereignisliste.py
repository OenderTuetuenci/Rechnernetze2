from heapq import *


class Ereignisliste:
    simulationtime = 0
    eventnummer = 0
    liste = []
    heapify(liste)

    @staticmethod
    def pop():
        if len(Ereignisliste.liste) > 0:
            return heappop(Ereignisliste.liste)
        else:
            return ()

    @staticmethod
    def push(event):
        Ereignisliste.eventnummer += 1
        heappush(Ereignisliste.liste, (event[0], event[1], Ereignisliste.eventnummer, event[2], event[3]))

    @staticmethod
    def start():
        while len(Ereignisliste.liste) != 0:
            if Ereignisliste.simulationtime > 450:
                break
            event = Ereignisliste.pop()
            Ereignisliste.simulationtime = event[0]
            event[3]()

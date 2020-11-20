from heapq import *

class Ereignisliste:
    simulationszeit = 0
    enummer = 0
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
        Ereignisliste.enummer += 1
        heappush(Ereignisliste.liste, (event[0], event[1], Ereignisliste.enummer ,event[2], event[3]))
    @staticmethod
    def start():
        while len(Ereignisliste.liste) != 0:
            if Ereignisliste.simulationszeit > 450:
                break
            event = Ereignisliste.pop()
            Ereignisliste.simulationszeit = event[0]
            event[3]()
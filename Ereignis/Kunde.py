from Ereignis.Ereignisliste import Ereignisliste as ev
from copy import deepcopy


class Kunde:
    kundenid = 0

    def __init__(self, typ, liste, interval):
        self.typ = typ
        self.liste = liste
        self.interval = interval

    def beginn(self):
        print(str(ev.simulationszeit) + "s " + str(self.typ) + str(self.kundenid) + "beginn")
        nextKunde = deepcopy(self)
        nextKunde.kundenid = self.kundenid + 1
        ev.push((ev.simulationszeit + self.liste[0][0], 3, self.ankunft, ["ankunft"]))
        ev.push((ev.simulationszeit + self.liste[0][0], 3, nextKunde.beginn, ["beginn"]))

    def ankunft(self):
        station = self.liste[0]
        print(str(ev.simulationszeit) + "s " + str(self.typ) + str(self.kundenid) + " ankunft " + str(station[3].name))

        if len(station[3].queue) < station[1]:
            station[3].queueIn(self)
        else:
            self.liste.pop(0)
            ev.push((ev.simulationszeit + station[0], 3, self.ankunft,["ankunft"]))

    def verlassen(self):
        station = self.liste.pop(0)
        print(str(ev.simulationszeit) + "s " + str(self.typ) + str(self.kundenid) + " verlassen " + str(station[3].name))
        if len(self.liste) <= 0:
            return
        station = self.liste[0]
        ev.push((ev.simulationszeit + station[0], 3, self.ankunft, ["ankunft"]))
        station[3].serve()



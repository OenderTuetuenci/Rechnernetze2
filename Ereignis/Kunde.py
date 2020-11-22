from Ereignis.Ereignisliste import Ereignisliste as eventList
from copy import deepcopy


class Kunde:
    customer_id = 0

    def __init__(self, typ, liste, interval):
        self.typ = typ
        self.liste = liste
        self.interval = interval

    def beginn(self):
        print(str(eventList.simulationtime) + "s " + str(self.typ) + str(self.customer_id) + " beginn")
        next_customer = deepcopy(self)
        next_customer.customer_id = self.customer_id + 1
        eventList.push((eventList.simulationtime + self.liste[0][0], 3, self.ankunft, ["ankunft"]))
        eventList.push((eventList.simulationtime + self.liste[0][0], 3, next_customer.beginn, ["beginn"]))

    def ankunft(self):
        station = self.liste[0]
        print(str(eventList.simulationtime) + "s " + str(self.typ) + str(self.customer_id) + " ankunft " + str(
            station[3].name))

        if len(station[3].queue) < station[1]:
            station[3].queueIn(self)
        else:
            self.liste.pop(0)
            eventList.push((eventList.simulationtime + station[0], 3, self.ankunft, ["ankunft"]))

    def verlassen(self):
        station = self.liste.pop(0)
        print(str(eventList.simulationtime) + "s " + str(self.typ) + str(self.customer_id) + " verlassen " + str(
            station[3].name))
        if len(self.liste) <= 0:
            return
        station = self.liste[0]
        eventList.push((eventList.simulationtime + station[0], 3, self.ankunft, ["ankunft"]))
        station[3].serve()

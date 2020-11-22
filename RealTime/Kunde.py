from threading import Thread,Event
from time import sleep,time

class Kunde(Thread):
    def __init__(self,stationMitTyp,name,ergebnis,startZeit):
        Thread.__init__(self)
        self.name = name
        self.stationMitTyp = stationMitTyp
        self.ergebnis = ergebnis
        self.startZeit = startZeit
        ergebnis.kundemImSupermarkt.append(self)

    def run(self):
        self.ergebnis.anzahlKunden += 1
        while len(self.stationMitTyp) >= 0:
            if len(self.stationMitTyp) == 0:
                self.ergebnis.kundemImSupermarkt.remove(self)
                break
            stationMitTyp = self.stationMitTyp.pop()
            station = stationMitTyp[0]
            typ = stationMitTyp[1]
            sleep(typ[0])

            if len(station.queue) < typ[2]:
                print(f"{time() - self.startZeit:.2f}: " + self.name + " Queueing at " + station.name)
                servEv = Event()
                station.ankommen((typ[1],servEv,self))
                station.arrEv.set()
                servEv.wait()
            else:
                print(f"{time() - self.startZeit:.2f}: " + self.name + " Dropped at " + station.name)
                self.ergebnis.verlorenKunden +=1
                self.ergebnis.verlorenStationDict[station] += 1





from collections import deque
from RealTime.Kunde import Kunde
from RealTime.Station import Station
from RealTime.Ergebnis import Ergebnis
import time
from threading import Thread,Event

def start_typ1(target_time, typ1, result, start_time):
    actual_time = time.time() - start_time
    countA = 1
    sleep_duration = 200/debug


    while actual_time < target_time:
        thread = Kunde(typ1.copy(), "A" + str(countA), result, start_time)
        countA += 1
        thread.start()
        time.sleep(sleep_duration)
        actual_time += sleep_duration
        if actual_time > 1800/debug:
            endEv.set()
            break


def start_typ2(target_time, typ2, result, start_time):
    actual_time = time.time() - start_time
    countB = 1
    sleep_duration = 60/debug

    time.sleep(1)
    while actual_time < target_time:
        thread = Kunde(typ2.copy(), "B" + str(countB), result, start_time)
        countB += 1
        thread.start()
        time.sleep(sleep_duration)
        actual_time += sleep_duration
        if actual_time > 1800/debug:
            endEv.set()
            break
debug = 1000
backer = Station("Bäcker", 10/debug)
wurst = Station("Wurst", 30/debug)
kase = Station("Käse", 60/debug)
kasse = Station("Kasse", 5/debug)

endEv = Event()
start = time.time()

backer.startZeit = start
wurst.startZeit = start
kase.startZeit = start
kasse.startZeit = start

backer.start()
wurst.start()
kase.start()
kasse.start()

typ1 = deque([(kasse, (60/debug, 30, 20)), (kase, (45/debug, 3, 5)), (wurst, (30/debug, 5, 10)), (backer, (10/debug, 10, 10))])
typ2 = deque([(backer, (20/debug, 3, 20)), (kasse, (30/debug, 3, 20)), (wurst, (30/debug, 2, 5))])

verlorenStationDict = {
    backer: 0,
    wurst: 0,
    kase: 0,
    kasse: 0
}

ergebnis = Ergebnis(verlorenStationDict)

start_thread_typ1 = Thread(target=start_typ1, args=(201, typ1, ergebnis, start))
start_thread_typ2 = Thread(target=start_typ2, args=(62, typ2, ergebnis, start))

start_thread_typ1.start()
start_thread_typ2.start()

time.sleep(10)
while len(ergebnis.kundemImSupermarkt) > 0:
    Lol = "lol"
ergebnis.endZeit = time.time()-start

drop_perc_baecker = ergebnis.verlorenStationDict[backer] / ergebnis.anzahlKunden * 100
drop_perc_wurst = ergebnis.verlorenStationDict[wurst] / ergebnis.anzahlKunden * 100
drop_perc_kaese = ergebnis.verlorenStationDict[kase] / ergebnis.anzahlKunden * 100
drop_perc_kasse = ergebnis.verlorenStationDict[kasse] / ergebnis.anzahlKunden * 100

print("Simulationsende: " + str(ergebnis.endZeit) + 's')
print("Anzahl Kunden: " + str(ergebnis.anzahlKunden))
print("Anzahl vollständige Einkäufe: " + str(ergebnis.anzahlKunden - ergebnis.verlorenKunden))
#print("Mittlere Einkaufsdauer: " + str(mediator_period) + 's')
print("Drop percentage at Bäcker: " + str(drop_perc_baecker))
print("Drop percentage at Metzger: " + str(drop_perc_wurst))
print("Drop percentage at Käse: " + str(drop_perc_kaese))
print("Drop percentage at Kasse: " + str(drop_perc_kasse))
print("Ende \n")


from Ereignis.Ereignisliste import Ereignisliste as ev
from Ereignis.Kunde import Kunde
from Ereignis.Station import Station

backer = Station("Bäcker",10)
wurst = Station("Wurst",30)
kase = Station("Käse",60)
kasse = Station("Kasse",5)

typ1 =  [(10, 10, 10, backer), (30, 10, 5, wurst), (45, 5, 3, kase), (60, 20, 30, kasse)]
kunde1 = Kunde("Typ1-", typ1, 200)

typ2 = [(30, 5, 2, wurst), (30, 20, 3, kasse), (20, 20, 3, backer)]
kunde2 = Kunde("Typ2-",typ2, 60)

ev.push((0, 2, kunde1.beginn, ["KT1-1", "beginn"]))
ev.push((1, 2, kunde2.beginn, ["KT2-1", "beginn"]))
ev.start()
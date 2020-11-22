from Ereignis.Ereignisliste import Ereignisliste as eventList
from Ereignis.Kunde import Kunde
from Ereignis.Station import Station

backer = Station("Bäcker", 10)
wurst = Station("Wurst", 30)
kase = Station("Käse", 60)
kasse = Station("Kasse", 5)

typ_01 = [(10, 10, 10, backer), (30, 10, 5, wurst), (45, 5, 3, kase), (60, 20, 30, kasse)]
customer_01 = Kunde("Typ1-", typ_01, 200)

typ_02 = [(30, 5, 2, wurst), (30, 20, 3, kasse), (20, 20, 3, backer)]
customer_02 = Kunde("Typ2-", typ_02, 60)

eventList.push((0, 2, customer_01.beginn, ["KT1-1", "beginn"]))
eventList.push((1, 2, customer_02.beginn, ["KT2-1", "beginn"]))
eventList.start()

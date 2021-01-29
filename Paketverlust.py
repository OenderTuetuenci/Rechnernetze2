puffergroße = int(input("Puffer (in Paketen): "))
ubertragungankommen = float(input("Uebertragungsverzögerung ankommend (in ms): "))
ubertragungsenden = float(input("Uebertragungsverzögerung abgehend (in ms): "))
anzahlPakete = float(input("Gesamte Anzahl zu sendende Pakete (in Pakete): "))
bereitsVerloren = input("bereits verloren Pakete (ggf voraufgabe, in Pakete): ").replace(" ", "").split(",")

import queue

queue = queue.Queue(puffergroße)

count = float(0)
paket = 1
verloren = []
while anzahlPakete > 0:
    if count % ubertragungsenden == 0.0 and not queue.empty():
        print("removed: ", queue.get())
    if count % ubertragungankommen == 0.0:
        if queue.full():
            print("verloren: ", paket)
            verloren.append(paket)
        else:
            queue.put(paket)
            print("ankommen: ", paket)
            if count == 0.0:
                print("removed: ", queue.get())
        paket += 1
        anzahlPakete -= 1
        while str(paket) in bereitsVerloren:
            paket += 1
            anzahlPakete -= 1
    count += 0.1
    count = round(count, 1)

print(verloren)

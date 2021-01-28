puffergroße = int(input("Puffer"))
ubertragungankommen = float(input("ubertragungankommen")) / 1000
ubertragungsenden = float(input("ubertragungsenden")) / 1000
anzahlPakete = float(input("anzahl Pakete"))

import queue

queue = queue.Queue(puffergroße)

import time
import threading
from threading import Thread

lock = threading.Lock()


def ankommen():
    paket = 1
    verloren = []
    global anzahlPakete
    while anzahlPakete > 0:
        if queue.full():
            print("verloren:",paket)
            verloren.append(paket)
        else:
            lock.acquire()
            queue.put(paket)
            print("ankommen:", paket)
            lock.release()
        paket += 1
        anzahlPakete = anzahlPakete - 1
        time.sleep(ubertragungankommen)
    print("verloren:",verloren)


def senden():
    while anzahlPakete > 0:
        if not queue.empty():
            lock.acquire()
            z = queue.get()
            lock.release()
            time.sleep(ubertragungsenden)


ankommenThread = Thread(target=ankommen).start()
sendenThread = Thread(target=senden).start()
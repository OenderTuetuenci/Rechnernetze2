from collections import deque
from threading import Thread, Event, Lock
from time import sleep,time

lock = Lock()

class Station(Thread):
    def __init__(self, name, processingTime):
        Thread.__init__(self)
        self.name = name
        self.processingTime = processingTime
        self.queue = deque([])
        self.amLaufen = False
        self.arrEv = Event()
        self.startZeit = 0

    def run(self):
        while True:
            self.arrEv.wait()
            if len(self.queue) > 0:
                task = self.leave()
                sleep(task[0] * self.processingTime)
                print(f"{time() - self.startZeit:.2f}: " + task[2].name + " Finished at " + self.name)
                task[1].set()
            else:
                self.arrEv.clear()

    def ankommen(self, task):
        lock.acquire()
        self.queue.append(task)
        lock.release()

    def leave(self):
        lock.acquire()
        task = self.queue.pop()
        lock.release()
        return task

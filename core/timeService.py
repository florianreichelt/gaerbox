import time

def waitUntil(nextTime, timeOut):
    t = time.perf_counter()
    tLimit = t + timeOut
    while (t < nextTime) and (t < tLimit):
        time.sleep(0.5)
        t = time.perf_counter()


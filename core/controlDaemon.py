import os
import errno
import sys
import threading
import json
import gaerbox
import time
import timeService
import queue


reqQueue = queue.Queue()
respQueue = queue.Queue()

reqFifo = '/tmp/gaerboxReqFifo'
respFifo = '/tmp/gaerboxRespFifo'

try:
    os.mkfifo(reqFifo)
    os.mkfifo(respFifo)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

class RequestListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):    
        while True:
            #print("opening gaerbox_control FIFO ...")
            with open(reqFifo) as fifo:
                print("  opened")
                while True:
                    data = fifo.read()
                    if len(data) == 0:
                        print("  writer closed")
                        break
                    print("  read: {0}".format(data))
                    self.processRequest(data)

    def processRequest(self, data):       
        dict = None
        try:
            dict = json.loads(data)
        except:
            print("Error: received non JSON request!")
        if dict:
            reqQueue.put(dict)
            
            resp = None
            i = 0
            while respQueue.empty() and i < 4*5:
                time.sleep(0.25)
                i += 1
            # TODO: implement ID matching for request/response pairs. If ID
            # does not match, then also report controlTimeout.
            if respQueue.empty():
                resp = {"response":"controlTimeout"}
            else:
                resp = respQueue.get()
            print("processRequest(): sending FIFO response ...")
            with open(respFifo, "w") as f:
                json.dump(resp, f)
            print("processRequest(): response sent")
        else:
            with open(respFifo, "w") as f:
                json.dump({ "response" : "inputError" }, f)

listener = RequestListener()
listener.setDaemon(True)
listener.start()

gb = gaerbox.Gaerbox()
gb.setTemperature(25.0)
gb.enableCtrl(False)

def pushResponse(respType, val=None):
    resp = None
    if val:
        resp = {"response":respType, "value":val}
    else:
        resp = {"response":respType}
    
    respQueue.put(resp)


def processRequest(request):    
    if request:
        cmd = request["cmd"]
        if cmd == "setTemperature":
            val = request["value"]
            print("setTemperature: value = " + str(val))
            gb.setTemperature(val)
            gb.enableCtrl(True)
            pushResponse("ack")
        elif cmd == "stopHeating":
            gb.enableCtrl(False)
            gb.reset()
            pushResponse("ack")
        elif cmd == "getTemperature":
            try:
                temp = gb.temperatureLog.last()
                pushResponse("ackValue", temp.toDict())
            except:
                pushResponse("nack")
        else:
            pushResponse("unsup")

controlInterval = 10.0
nextControlTime = time.perf_counter() + controlInterval
try:
    while True:
        request = None
        if not reqQueue.empty():
            request = reqQueue.get()

        processRequest(request)
        time.sleep(0.25)

        #timeService.waitUntil(currentTime + 10.0, 12.0)

        currentTime = time.perf_counter()
        if currentTime > nextControlTime:
            nextControlTime = currentTime + controlInterval
            gb.update()
            print("Temp: " + gb.temperatureLog.last().toJSON())
except KeyboardInterrupt:
    print("Interrupt by user")
except Queue.Full:
    print("Received Queue.Full exception. Aborting")
except Queue.Empty:
    print("Received Queue.Empty exception. Aborting")
except:
    print("Unhandled exception! Aborting execution now!")
finally:
    print("Exiting ...")
    gb.cleanup()
    sys.exit()


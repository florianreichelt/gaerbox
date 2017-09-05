import os
import errno
import sys
import threading
import json
import gaerbox
import time
import timeService

reqCV = threading.Condition()
respCV = threading.Condition()
reqs = []
resps = []

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
            print("opening gaerbox_control FIFO ...")
            with open(reqFifo) as fifo:
                print("  opened")
                while True:
                    data = fifo.read()
                    if len(data) == 0:
                        print("  writer closed")
                        break
                    print('  read: "{0}"'.format(data))
                    self.processRequest(data)

    def processRequest(self, data):       
        dict = None
        try:
            dict = json.loads(data)
        except:
            print("Error: received non JSON request!")
        if dict:
            with reqCV:
                reqs.append(dict)
                reqCV.notify()
            
            resp = None
            with respCV:
                while len(resps) == 0:
                    print("processRequest(): waiting for response data")
                    respCV.wait()
                resp = resps.pop(0)

            f = open(respFifo, "w")
            json.dump(resp, f)
            f.close()
            print("processRequest(): sent response")


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
    with respCV:
        resps.append(resp)
        respCV.notify()


def processRequest(request):    
    if request:
        cmd = request["cmd"]
        if cmd == "setTemperature":
            val = cmd["value"]
            print("setTemperature: value = " + str(val))
            gb.setTemperature(val)
            pushResponse("ack")
        elif cmd == "stopHeating":
            gb.reset()
            pushResponse("ack")
        elif cmd == "getTemperature":
            temp = gb.temperatureLog.last()
            pushResponse("ackValue", temp.toDict())
        else:
            pushResponse("unsup")


currentTime = time.perf_counter()
try:
    while True:
        request = None
        with reqCV:
            if len(reqs) != 0:
                request = reqs.pop(0)

        processRequest(request)
        timeService.waitUntil(currentTime + 10.0, 12.0)
        currentTime = time.perf_counter()
        gb.update()

        print("Temp: " + gb.temperatureLog.last().toJSON())
except KeyboardInterrupt:
    gb.cleanup()
    sys.exit()

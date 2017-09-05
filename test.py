#!/usr/bin/python

import gaerbox
import time
import sys

gb = gaerbox.Gaerbox()
gb.setTemperature(30.0)
gb.enableCtrl(True)

try:
    while True:
        gb.update()
        print "Temp: " + gb.temperatureLog.last().toJSON()
        time.sleep(10)
except KeyboardInterrupt:
    gb.cleanup()
    sys.exit()


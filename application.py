#!/usr/bin/python

import control
import time
import sys

sensor = control.GaerboxSensor()
heater = control.Heating()
logger = control.TempLogger("log.txt")

heater.set(100)

try:
    while True:
        sensor.update()
        value = sensor.getValue()
        print value.toJson()
        logger.push(value)

        time.sleep(1)
except KeyboardInterrupt:
    logger.writeFile()
    sys.exit()


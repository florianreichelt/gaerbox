#!/usr/bin/python

import control
import time
import sys
import json
import os

sensor = control.GaerboxSensor()
heater = control.Heating()
logger = control.TemperatureLog()

heater.set(100)

try:
    while True:
        sensor.update()
        value = sensor.getValue()
        print(value.toJSON())
        logger.push(value)

        time.sleep(1)
except KeyboardInterrupt:
    num = 0
    filename = lambda num: "logs/temperature" + str(num) + ".log"
    while os.path.isfile(filename(num)):
        num += 1
    if len(logger.measurements):
        f = open(filename(num), "w")
        json.dump(logger.toDict(), f)
    sys.exit()


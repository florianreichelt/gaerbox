#!/usr/bin/python

import RPi.GPIO as GPIO
import gaerboxBase
import os
import re
import json
import datetime


class Heating:
    def __init__(self):
        self.pinNumber = 11
        self.pwmFreq = 100
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinNumber, GPIO.OUT)
        self.controlPin = GPIO.PWM(self.pinNumber, 100)

    def set(self, val):
        if val < 0 or val > 100 or not isinstance(val, int):
            raise GaerboxException("Parameter 'val' not valid")

        self.controlPin.start(val)

    def stop(self):
        self.controlPin.stop()

    def cleanup(self):
        GPIO.cleanup()


class Time:
    def __init__(self, hour, min, sec):
        self.hour = hour
        self.min = min
        self.sec = sec

    def toJson(self):
        dict = { "hour" : self.hour, "min" : self.min, "sec" : self.sec }
        return json.dumps(dict)


class Temperature:
    def __init__(self, temp, time):
        self.temp = temp
        self.time = time

    def setTemp(self, temp):
        self.temp = temp

    def setTime(self, time):
        self.hour = hour
        self.time = time

    def getTemp(self):
        return self.temp

    def getTime(self):
        return self.time

    def toJson(self):
        timeObj = self.time.toJson()
        timeDict = json.loads(timeObj)
        dict = { "temp" : self.temp, "time" : timeDict }
        return json.dumps(dict)

    #def fromJson(self, obj):
        #dict = json.loads(obj)
        #self.time


class TempSensor:
    def __init__(self, deviceNumber):
        self.deviceNumber = deviceNumber
        self.deviceFilename = "/sys/bus/w1/devices/" + deviceNumber + "/w1_slave"
        if not os.path.isfile(self.deviceFilename):
            raise GaerboxException("device file not found")

    def update(self):
        ret = False
        file = open(self.deviceFilename, "r")
        line = file.readline()
        if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
            line = file.readline()
            m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
            if m:
                temp = float(m.group(2)) / 1000.0
                #print "the value: " + str(value)
                self.setValue(temp)
                ret = True
        file.close()
        return ret

    def setValue(self, value):
            time = datetime.datetime.now()
            time = Time(time.hour, time.minute, time.second)
            self.value = Temperature(value, time)

    def getValue(self):
        return self.value


class GaerboxSensor(TempSensor):
    def __init__(self):
        TempSensor.__init__(self, "10-000803197736")


class TempLogger:
    measurements = []

    def __init__(self, filename):
        self.filename = filename

    #def measurementToJson(self, measurement):


    def push(self, measurement):
        self.measurements.append(measurement)

    def getMeasurements(self):
        return self.measurements

    def getLastMeasurement(self):
        if len(self.measurements):
            return self.measurements[len(self.measurements) - 1]
        raise GaerboxException("Out of bounds")

    #def getJson(self):
        #list = []
        #for meas in self.measurements:
            #list.append(json.load(meas.toJson()))
        #return list

    def writeFile(self):
        file = open(self.filename, "w")
        file.write("[\n")
        for i in range(0, len(self.measurements)):
            file.write("  " + self.measurements[i].toJson())
            if i < len(self.measurements)-1:
                file.write(",\n")
            else:
                file.write("\n")
        file.write("]")
        file.close()

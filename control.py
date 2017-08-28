#!/usr/bin/python

import RPi.GPIO as GPIO
import os
import re
import json


class GaerboxException(Exception):
	def __init__(self, msg):
		self.msg = msg


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
		

class TempSensor:
	value = 0.0

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
				self.value = float(m.group(2)) / 1000.0
				ret = True
		file.close()
		return ret

	def getValue(self):
		return self.value


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

	def fromJson(self, obj):
		dict = json.loads(obj)
		#self.time


class TempLogger:
	measurements = []		

	def __init__(self, filename):
		self.file = open(filename, "a")

	#def measurementToJson(self, measurement):
		

	def push(self, measurement):
		self.measurements.append(measurement)
		
	def getMeasurements(self):
		return self.measurements

	def getLastMeasurement(self):
		if len(self.measurements):
			return self.measurements[len(self.measurements) - 1]
		raise GaerboxException("Out of bounds")


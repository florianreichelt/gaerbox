import control
from mypid import PIDControl
from control import GaerboxSensor, TemperatureLog, Temperature, Time, Heating
import json

class Gaerbox:
    def __init__(self):
        self.pid = PIDControl(0.3, 0.003, 11.0)
        self.pid.setSampleTime(10.0)
        self.pid.setWindup(180)
        self.temperatureSetPoint = 0
        self.active = False
        self.sensor = GaerboxSensor()
        self.temperatureLog = TemperatureLog()
        self.heating = Heating()

    def reset(self):
        self.pid.reset()
        self.active = False
        self.temperatureSetPoint = 0
        self.heating.set(0)
        self.heating.stop()

    def enableCtrl(self, val):
        if val:
            # reset PID
            self.active = True
            self.pid.reset()
        else:
            self.reset()

    def update(self):
        if self.sensor.update():
            self.temperature = self.sensor.getValue()
            self.temperatureLog.push(self.temperature)
            if self.active:
                self.pid.doControl(self.temperature.temp)
                output = self.pid.output
                self.heating.set(int(100.0 * output))
    
    def setTemperature(self, temp):
        self.temperatureSetPoint = temp
        self.pid.setSetPoint(temp)

    def saveLog(self):
        f = open("logs/gaerbox.log", "w")
        json.dump(self.temperatureLog.toDict(), f)

    def cleanup(self):
        self.reset()
        self.saveLog()


class CommandHandler:
    def __init__(self, gaerbox):
        self.gaerbox = gaerbox

    def process(self, obj):
        if obj["cmd"] == "setTemperature":
            val = float(obj["value"])
            self.gaerbox.setTemperature(val)
            ret = {"responseType": "ack"}
            return ret
        else:
            print("Received unsupported cmd request")
            return {"responseType": "unsupported_cmd"}

    def update(self):
        self.gaerbox.update()


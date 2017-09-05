class PIDControl:
    windup = 100.0
    sampleTime = 0.0

    def __init__(self, Kp = 1.0, Ki = 0.0, Kd = 0.0):
        self.Kp = float(Kp)
        self.Ki = float(Ki)
        self.Kd = float(Kd)
        self.IVal = float(0)
        self.lastError = float(0)
        self.setPoint = float(0)

    def setSampleTime(self, sampleTime):
        self.sampleTime = float(sampleTime)

    def setWindup(self, windup):
        self.windup = float(windup)

    def setSetPoint(self, setPoint):
        self.setPoint = float(setPoint)

    def doControl(self, processVal):
        curError = self.setPoint - processVal

        self.PVal = curError

        self.IVal += curError * self.sampleTime
        if self.IVal > self.windup:
            self.IVal = self.windup
        elif self.IVal < -self.windup:
            self.IVal = -self.windup

        self.DVal = (curError - self.lastError) / self.sampleTime

        self.output = self.Kp * self.PVal + self.Ki * self.IVal + self.Kd * self.DVal

        if self.output > 1.0:
            self.output = 1.0
        elif self.output < 0.0:
            self.output = 0.0

        self.lastError = curError

    def getOutput(self):
        return self.output

    def reset(self):
        self.IVal = 0.0
        self.lastError = 0.0


import matplotlib.pyplot as plt
import json
from mypid import PIDControl
import numpy as np
from controlCurve import ControlCurve, CurvePart


Kp = 0.3
Ki = 0.003
Kd = 11.0
pid = PIDControl(Kp, Ki, Kd)
pid.setSampleTime(10.0)
pid.setWindup(180)

sysImpulse = np.fromfile("sysImpulse.nparray")


def stripImpulse(f_input):
    l_ret = []
    for i in range(0, 1500):
        l_ret.append(float(f_input[i]))
    return l_ret


def simulationStep(i, systemOutputs, systemImpulse, systemInitial, systemInputs):
    systemOutputs[i] = systemInitial
    past = min([len(systemImpulse), i+1])
    for j in range(0, past):
        systemOutputs[i] += systemInputs(i-j)*systemImpulse[j]

curve = ControlCurve([
    CurvePart(3600, 27, 0),
    CurvePart(3600, 30, -(1.0 / 3600) * 5.0),
    CurvePart(3600, 22, 0),
    CurvePart(60*15, 22, (1.0 / (60*15)) * 13.0),
    CurvePart(3600, 35, 0)
])
setPointFunc = lambda x: curve.sample(x)

simTime = 4 * 3600 + 15*60

sysOutputs = np.zeros(simTime, dtype=np.float)
sysTimes = np.zeros(simTime, dtype=np.int)
sysInputs = np.zeros(simTime, dtype=np.float)
sysSetPoints = np.zeros(simTime, dtype=np.float)
sysInitial = 22.175


sysSetPoint = 30
sysOutput = sysInitial

stepIndex = 0
for stepIndex in range(0, simTime):
    sysSetPoint = setPointFunc(stepIndex)
    sysSetPoints[stepIndex] = sysSetPoint

    pid.setSetPoint(sysSetPoint)
    if 0 == (stepIndex % 10):
        pid.doControl(sysOutput)
        ctrlOutput = pid.output
        if ctrlOutput > 1.0:
            ctrlOutput = 1.0
        if ctrlOutput < 0.0:
            ctrlOutput = 0.0

    sysInputs[stepIndex] = ctrlOutput
    sysTimes[stepIndex] = stepIndex

    inputLambda = lambda i: sysInputs[i]

    simulationStep(stepIndex, sysOutputs, sysImpulse, sysInitial, inputLambda)

    sysOutput = sysOutputs[stepIndex]


plt.figure(0)
plt.subplot(211)
plt.plot(sysTimes, sysOutputs, label="system output")
plt.plot(sysTimes, sysSetPoints, label="setpoint")
plt.legend()
plt.subplot(212)
plt.plot(sysTimes, sysInputs, label="system input (ctrl output")
plt.legend()
plt.show()

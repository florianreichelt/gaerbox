import matplotlib.pyplot as plt
import json
from mypid import PIDControl
import numpy as np


Kp = 0.3
Ki = 0.005
Kd = 1.1
pid = PIDControl(Kp, Ki, Kd)
pid.setSampleTime(1.0)
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


def setPointFunc(x):
    l_const1 = 30.0
    l_const2 = 30.0
    l_const3 = 22.0
    l_const4 = 22.0
    l_const5 = 35.0

    l_ival1 = 60 * 60
    l_ival2 = 60 * 60
    l_ival3 = 60 * 60
    l_ival4 = 60 * 15
    l_ival5 = 60 * 60

    l_lin1 = 0.0
    l_lin2 = -(1.0 / l_ival2) * 5.0
    l_lin3 = 0.0
    l_lin4 = (1.0 / l_ival4) * 13.0
    l_lin5 = 0.0

    l_ret = 0
    if x < l_ival1:
        l_ret = l_const1
    elif x < l_ival1 + l_ival2:
        l_ret = l_const2 + l_lin2*(x - l_ival1)
    elif x < l_ival1 + l_ival2 + l_ival3:
        l_ret = l_const3
    elif x < l_ival1 + l_ival2 + l_ival3 + l_ival4:
        l_ret = l_const4 + l_lin4*(x - (l_ival1 + l_ival2 + l_ival3))
    elif x < l_ival1 + l_ival2 + l_ival3 + l_ival4 + l_ival5:
        l_ret = l_const5
    return l_ret

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

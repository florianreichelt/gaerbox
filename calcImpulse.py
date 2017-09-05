import matplotlib.pyplot as plt
import json
import numpy as np
from scipy.optimize import curve_fit

file = open("Z:/log_heating2.txt")

data = json.load(file)

dataTemp = []
dataTime = []
l_tmpTime = 0
for meas in data:
    dataTemp.append(float(meas["temp"]))
    dataTime.append(l_tmpTime)
    l_tmpTime = l_tmpTime + 1


def filter(f_data, f_window):
    l_ret = []
    for i in range(0, len(f_data)-f_window):
        l_tmp = 0.0;
        for j in range(0, f_window):
            l_tmp = l_tmp + float(f_data[i + j])
        l_ret.append(l_tmp / float(f_window))
    for i in range(0, f_window):
        l_ret.append(f_data[len(f_data) - f_window + i])
    return l_ret

tempFilter = filter(dataTemp, 10)


tempGradient = np.gradient(np.array(tempFilter, dtype=np.float))


plt.figure(0)
plt.subplot(211)
plt.plot(dataTime, dataTemp, label="unfiltered")
plt.plot(dataTime, tempFilter, label="filtered")
plt.legend()


plt.subplot(212)
plt.plot(dataTime, tempGradient, label="gradient of filtered")
plt.legend()
plt.show()


fileGrad = open("sysImpulse.nparray", "w")

tempGradient.tofile(fileGrad)

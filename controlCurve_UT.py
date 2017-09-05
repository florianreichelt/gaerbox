import controlCurve as c
import matplotlib.pyplot as plt
import numpy as np

p1 = c.CurvePart(100, 30, 0)
p2 = c.CurvePart(50, 30, -5.0*(1.0/50.0))
p3 = c.CurvePart(150, 25, 0)

curve = c.ControlCurve([p1, p2, p3])

xValues = np.zeros(200)
yValues = np.zeros(200)

for i in range(0, len(xValues)):
    xValues[i] = i
    yValues[i] = curve.sample(i)

plt.figure(0)
plt.plot(xValues, yValues)
plt.show()

print(p1.toJSON())
print(curve.toJSON())

testJson = p1.toJSON()
p4 = c.CurvePartJSON(testJson)
print(p4.length)
import json
from gaerboxBase import JSONSerializable, JSONDeserializable, GaerboxException

class CurvePart(JSONSerializable):
    def __init__(self, length, constant, slope):
        self.length = length
        self.constant = float(constant)
        self.slope = float(slope)

    def sample(self, x):
        if x >= self.length:
            raise GaerboxException("CurvePart: out of definition range")
        return self.constant + float(x) * self.slope

    def toDict(self):
        return {"length": self.length, "constant": self.constant, "slope": self.slope}


class CurvePartJSON(CurvePart, JSONDeserializable):
    def __init__(self, jsonStr):
        self.fromJSON(jsonStr)

    def fromJSON(self, jsonStr):
        dict = json.loads(jsonStr)
        length = int(dict["length"])
        constant = float(dict["constant"])
        slope = float(dict["slope"])
        super(CurvePartJSON, self).__init__(length, constant, slope)


class ControlCurve(JSONSerializable):
    def __init__(self, data):
        self.parts = data
        self.lengths = []
        lengths = 0
        for i in range(0, len(self.parts)):
            lengths += self.parts[i].length
            self.lengths.append(lengths)

    def sample(self, x):
        pos = -1
        length = 0
        for i in range(0, len(self.lengths)):
            if (x >= length) & (x < self.lengths[i]):
                pos = i
                break
            length = self.lengths[i]
        if pos == -1:
            raise GaerboxException("ControlCurve: out of definition range")
        return self.parts[pos].sample(x - length)

    def toDict(self):
        ret = []
        for i in range(len(self.parts)):
            ret.append(self.parts[i].toDict())
        return ret


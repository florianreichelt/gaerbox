import json

class GaerboxException(Exception):
    def __init__(self, msg):
        self.msg = msg

class JSONSerializable:
    def toDict(self):
        raise GaerboxException("toDict not implemented by child class")

    def toJSON(self):
        return json.dumps(self.toDict())


class JSONDeserializable:
    def fromJSON(self, jsonStr):
        raise GaerboxException("fromJSON not implemented by child class")

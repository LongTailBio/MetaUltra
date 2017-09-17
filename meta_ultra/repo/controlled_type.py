
class ControlledTypeNotFoundError(Exception):
    pass

class ControlledType():
    def __init__(self, typeStr):
        self.allowedStrings = {allowed for allowed in self.allowedStrings()}
        self._checkType( typeStr)
        self.typeStr = typeStr


    def _checkType(self, typeStr):
        if typeStr not in self.allowedStrings:
            raise ControlledTypeNotFoundError()
        
    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.typeStr == other.typeStr

    def __str__(self):
        return self.typeStr

    def allowedStrings(self):
        raise NotImplementedError()

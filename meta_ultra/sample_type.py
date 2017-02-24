from enum import Enum

class SampleTypeNotFoundError(Exception):
    pass

class SampleType(Enum):
    ENVIROMENTAL_MICROBIOME='ENVIROMENTAL_MICROBIOME'
    PHONE_MICROBIOME='PHONE_MICROBIOME'

    @classmethod
    def asSampleType(ctype, val):
        if type(val) == str:
            return ctype.fromString(val)
        return val

    @classmethod
    def asString(ctype, val):
        if type(val) != str:
            return ctype.toString(val)
        return val
    
    @classmethod
    def toString(ctype, val):
        for k,v in ctype.__members__.items():
            if val == v:
                return k
    
    @classmethod
    def fromString(ctype, string):
        for k,v in ctype.__members__.items():
            if string == k:
                return v

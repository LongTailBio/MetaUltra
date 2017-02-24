from enum import Enum

class DataTypeNotFoundError(Exception):
    pass

class DataType(Enum):
    DNA_SEQ_SINGLE_END='DNA_SEQ_SINGLE_END'
    DNA_SEQ_PAIRED_END='DNA_SEQ_PAIRED_END'

    @classmethod
    def asDataType(ctype, val):
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

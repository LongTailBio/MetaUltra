from enum import Enum

class DataTypeNotFoundError(Exception):
    pass

class DataType(Enum):
    SR_WMGS_DNA_SINGLE_END='SR_WMGS_DNA_SINGLE_END'
    SR_WMGS_DNA_PAIRED_END='SR_WMGS_DNA_PAIRED_END'
    LR_WMGS_ONT_DNA='LR_WMGS_ONT_DNA'
    RC_WMGS_10X_DNA='RC_WMGS_10X_DNA'
    SR_WMTS_RNA_SINGLE_END='SR_WMTS_RNA_SINGLE_END'
    SR_WMTS_RNA_PAIRED_END='SR_WMTS_RNA_PAIRED_END'
    
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

import meta_ultra.config as config
from meta_ultra.data_type import *

def toNameList(l):
    if not l:
        return []
    names = []
    for el in l:
        if not el:
            pass
        elif type(el) == str:
            names.append(el)
        else:
            names.append(el.name)
    return names

def toName(record):
    if type(record) == str:
        return record
    return record.name()

def convertDataTypes(dataTypes):
    if not dataTypes:
        return []
    out = []
    for dataType in dataTypes:
        if dataType:
            out.append( convertDataType(dataType))
    return out

def convertDataType(dataType):
    if type(dataType) == DataType:
        return dataType
    try:
        return DataType.fromString(dataType)
    except:
        raise DataTypeNotFoundError()

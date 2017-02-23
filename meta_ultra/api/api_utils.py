import meta_ultra.config as config


def toNameList(l):
    if not l:
        return []
    names = []
    for el in l:
        if type(el) == str:
            names.append(el)
        else:
            names.append(el.name)
    return names

def toName(record):
    if type(record) == str:
        return record
    return record.name()

def convertDataTypes(dataTypes):
    out = []
    for dataType in dataTypes:
        try:
            out.append( DataType[dataType])
        except:
            raise DataTypeNotFoundError()
    return out

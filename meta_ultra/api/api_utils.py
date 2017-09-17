import meta_ultra.config as config
from meta_ultra.data_type import *

def toNameSet(l):
    if not l:
        return set()
    names = set()
    for el in l:
        if not el:
            continue
        elif type(el) == str:
            names.add(el)
        else:
            names.add(toName(el))
    return names

def toName(record):
    if type(record) == str:
        return record
    return record.name()

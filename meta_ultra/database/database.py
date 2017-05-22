from tinydb import TinyDB, Query, where
import meta_ultra.config as config
from meta_ultra.data_type import DataType, DataTypeNotFoundError
from meta_ultra.sample_type import SampleType, SampleTypeNotFoundError
from meta_ultra.utils import *
from os.path import basename
import json

projectTbl = config.db_project_table
sampleTbl = config.db_sample_table
dataTbl = config.db_data_table
experimentTbl = config.db_experiment_table
resultTbl = config.db_result_table
confTbl = config.db_conf_table

################################################################################
#
# Classes
#
################################################################################

class RecordExistsError(Exception):
    pass

class NoSuchRecordError(Exception):
    pass

class InvalidRecordStateError(Exception):
    pass

class Record:
    dbTbl = None
    def __init__(self, name):
        self.name = name
        self.fileNames = []
        assert self.fileStatus()
        
    def registerFile(self, fname):
        self.fileNames.append(fname)

    def fileStatus(self):
        for file in self.fileNames:
            if not os.path.isfile(file):
                return False
        return True
        
    def record(self):
        rec = type(self).dbTbl().get(where('name') == self.name)
        if not rec:
            raise NoSuchRecordError()
        return rec

    def saved(self):
        return type(self).exists(self.name)
    
    def save(self,modify=False):
        if not self.validStatus():
            raise InvalidRecordStateError()
        
        if self.saved() and not modify:
            raise RecordExistsError()
        elif self.saved() and modify:
            rec = self.record()
            mydict = self.to_dict()
            for k,v in mydict.items():
                if k in rec and type(v) == dict and type(rec[k]) == dict:
                    for subk, subv in v.items():
                        rec[k][subk] = subv
                else:
                    rec[k] = v
            type(self).dbTbl().update(rec, eids=[rec.eid])
            return type(self).get(self.name)
        else:
            type(self).dbTbl().insert(self.to_dict())
            return type(self).get(self.name)

    
    def remove(self):
        record = self.record()
        type(self).dbTbl().remove(eids=[record.eid])

    def validStatus(self):
        return True

    @classmethod
    def build(ctype, *args, **kwargs):
        return ctype(**kwargs)

        
    @classmethod
    def get(ctype, name):
        rec = ctype.dbTbl().get(where('name') == name)
        if not rec:
            raise NoSuchRecordError()
        return ctype.build(**rec)

    @classmethod
    def exists(ctype, name):
        return ctype.dbTbl().get(where('name') == name) != None

    @classmethod
    def all(ctype):
        recs = ctype.dbTbl().all()
        recs = [ctype.build(**rec) for rec in recs]
        return recs

    @classmethod
    def search(ctype, query):
        recs = ctype.dbTbl().search(query)
        recs = [ctype.build(**rec) for rec in recs]
        return recs

    

    
class Conf(Record):
    def __init__(self, **kwargs):
        super(Conf, self).__init__(kwargs['name'])
        self.confDict = kwargs['conf_dict']

    def to_dict(self):
        out = {
            'name': self.name,
            'conf_dict': self.confDict
            }
        return out

    def __str__(self):
        return self.name
    
    @staticmethod
    def dbTbl():
        return confTbl()

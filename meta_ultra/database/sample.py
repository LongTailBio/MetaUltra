from tinydb import TinyDB, Query, where
import meta_ultra.config as config
from meta_ultra.data_type import DataType, DataTypeNotFoundError
from meta_ultra.sample_type import SampleType, SampleTypeNotFoundError
from meta_ultra.utils import *
from os.path import basename
import json
from .database import *
from .project import *

sampleTbl = config.db_sample_table
        
class Sample(Record):
    def __init__(self,**kwargs):
        super(Sample, self).__init__(kwargs['name'])
        self.projectName = kwargs['project_name']
        self.sampleType = SampleType.asSampleType(kwargs['sample_type'])
        if 'metadata' in kwargs and kwargs['metadata']:
            self.metadata = kwargs['metadata']
        else:
            self.metadata = {}

    def to_dict(self):
        out = {
            'name' : self.name,
            'project_name':self.projectName,
            'sample_type':SampleType.asString(self.sampleType),
            'metadata':self.metadata
            }
        return out

    def validStatus(self):
        try:
            Project.get(self.projectName)
        except NoSuchRecordError:
            return False
        return True

    
    def __str__(self):
        out = '{}\t{}'.format(self.name, self.projectName)
        for k, v in self.metadata.items():
            if ' ' in str(v):
                out += '\t{}="{}"'.format(k,v)
            else:
                out += '\t{}={}'.format(k,v)
        return out

    @staticmethod
    def dbTbl():
        return sampleTbl()


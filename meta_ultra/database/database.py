from tinydb import TinyDB, Query, where
import meta_ultra.config as config
from meta_ultra.config import DataType, DataTypeNotFoundError
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

def asDataType(dataType):
    if type(dataType) == DataType:
        return dataType
    try:
        return DataType.fromString(dataType)
    except:
        raise DataTypeNotFoundError() 

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
        if not self.validStatus:
            raise InvalidRecordStateError()
        
        if self.saved() and not modify:
            raise RecordExistsError()
        elif modify:
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


    
################################################################################



class Data( Record):
    def __init__(self, name, dataType, sampleName, projectName, experimentName):
        super(Data, self).__init__(name)
        self.dataType = asDataType(dataType)
        self.sampleName = sampleName
        self.projectName = projectName
        self.experimentName = experimentName
        
    def to_dict(self):
        out = {
            'name': self.name,
            'data_type': DataType.toString(self.dataType),
            'sample_name':self.sampleName,
            'project_name': self.projectName,
            'experiment_name':self.experimentName
            }
        self._to_dict(out)
        return out

    def validStatus(self):
        try:
            Sample.get(self.sampleName)
            Project.get(self.projectName)
            Experiment.get(self.experimentName)
        except NoSuchRecordError:
            return False
        return True
    
    @staticmethod
    def dbTbl():
        return dataTbl()

    @classmethod
    def build(ctype, *args, **kwargs):
        dataType = asDataType( kwargs['data_type'])
        if dataType == DataType.DNA_SEQ_SINGLE_END:
            return SingleEndDNASeqData(**kwargs)
        elif dataType == DataType.DNA_SEQ_PAIRED_END:
            return PairedEndDNASeqData(**kwargs)
        else:
            raise DataTypeNotFoundError()
    
class SingleEndDNASeqData(Data):
    def __init__(self,**kwargs):
        super(SingleEndDNASeqData, self).__init__(kwargs['name'],
                                                 type(self).dataType(),
                                                 kwargs['sample_name'],
                                                 kwargs['project_name'],
                                                 kwargs['experiment_name'])
        self.reads1 = kwargs['reads_1']
        self.registerFile(self.reads1)
        self.aveReadLen = int(kwargs['ave_read_length'])

    def _to_dict(self, out):
        out['reads_1'] = self.reads1
        out['ave_read_length'] = self.aveReadLen
        return out

    def __str__(self):
        out = '{}\t{}\t{}\t{}'.format(self.name, self.dataType,self.experimentName,self.reads1)
        return out

    @staticmethod
    def dataType():
        return DataType.DNA_SEQ_SINGLE_END

class PairedEndDNASeqData(Data):
    def __init__(self,**kwargs):
        super(PairedEndDNASeqData, self).__init__(kwargs['name'],
                                                 type(self).dataType(),
                                                 kwargs['sample_name'],
                                                 kwargs['project_name'],
                                                 kwargs['experiment_name'])
        self.reads1 = kwargs['reads_1']
        self.registerFile(self.reads1)
        self.reads2 = kwargs['reads_2']
        self.registerFile(self.reads2)
        self.aveReadLen = int(kwargs['ave_read_length'])
        try:
            self.aveGapLen = int(kwargs['ave_gap_length'])
        except (TypeError, KeyError):
            self.aveGapLen = None
            
    def _to_dict(self, out):
        out['reads_1'] = self.reads1
        out['reads_2'] = self.reads2
        out['ave_read_length'] = self.aveReadLen
        out['ave_gap_length'] = self.aveGapLen
        return out

    def __str__(self):
        out = '{}\t{}\t{}\t{}\t{}'.format(self.name, self.dataType,self.experimentName,self.reads1,self.reads2)
        return out

    @staticmethod
    def dataType():
        return DataType.DNA_SEQ_PAIRED_END


################################################################################

class Experiment(Record):
    def __init__(self, name, dataType):
        super(Experiment, self).__init__(name)
        self.dataType = asDataType(dataType)

    def to_dict(self):
        out = {
            'name': self.name,
            'data_type': DataType.toString( self.dataType)
        }
        self._to_dict(out)
        return(out)

    @staticmethod
    def dbTbl():
        return experimentTbl()

    @classmethod
    def build(ctype, *args, **kwargs):
        dataType = asDataType( kwargs['data_type'])
        if dataType == DataType.DNA_SEQ_SINGLE_END:
            return SingleEndDNASeqRun(**kwargs)
        elif dataType == DataType.DNA_SEQ_PAIRED_END:
            return PairedEndDNASeqRun(**kwargs)
        else:
            raise DataTypeNotFoundError()


    
class SingleEndDNASeqRun( Experiment):
    def __init__(self,**kwargs):
        super(SingleEndDNASeqRun, self).__init__(kwargs['name'],
                                                       DataType.DNA_SEQ_SINGLE_END)
        self.metadata = kwargs['metadata']

    def _to_dict(self,out):
        out['metadata'] = self.metadata
        return out

class PairedEndDNASeqRun( Experiment):
    def __init__(self,**kwargs):
        super(PairedEndDNASeqRun, self).__init__(kwargs['name'],
                                                       DataType.DNA_SEQ_PAIRED_END)
        self.metadata = kwargs['metadata']

    def _to_dict(self,out):
        out['metadata'] = self.metadata
        return out



    
################################################################################
        
class Sample(Record):
    def __init__(self,**kwargs):
        super(Sample, self).__init__(kwargs['name'])
        self.projectName = kwargs['project_name']
        if 'metadata' in kwargs:
            self.metadata = kwargs['metadata']
        else:
            self.metadata = {}

    def to_dict(self):
        out = {
            'name' : self.name,
            'project_name':self.projectName,
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

################################################################################
        
class Project(Record):
    def __init__(self,**kwargs):
        super(Project, self).__init__(kwargs['name'])
        if 'metadata' in kwargs:
            self.metadata = kwargs['metadata']
        else:
            self.metadata = {}

    def to_dict(self):
        out = {
            'name' : self.name,
            'metadata':self.metadata
            }
        return out

    def __str__(self):
        out = '{}'.format(self.name)
        for k, v in self.metadata.items():
            if ' ' in str(v):
                out += '\t{}="{}"'.format(k,v)
            else:
                out += '\t{}={}'.format(k,v)
        return out

    @staticmethod
    def dbTbl():
        return projectTbl()

    
    
################################################################################

class Result(Record):
    def __init__(self, **kwargs):
        super(Result, self).__init__(kwargs['name'])
        self.projectName = kwargs['project_name']
        self.sampleName = kwargs['sample_name']
        self.dataName = kwargs['data_name']
        self.confName = kwargs['conf_name']
        self.resultFiles = []
        for file in kwargs['result_files']:
            self.resultFiles.append(file)
            self.registerFile(file)

    def status(self):
        return self.fileStatus()
            
    def to_dict(self):
        out = {
            'name': self.name,
            'project_name': self.projectName,
            'sample_name': self.sampleName,
            'data_name': self.dataName,
            'conf_name': self.confName,
            'result_files':self.resultFiles
            }
        return out

    def validStatus(self):
        try:
            Sample.get(self.sampleName)
            Project.get(self.projectName)
            Experiment.get(self.experimentName)
            Data.get(self.dataName)
        except NoSuchRecordError:
            return False
        return True

    
    def __str__(self):
        out = '{}\t{}\t{}\t{}\t{}\t{}'.format(self.name,
                                              self.projectName,
                                              self.sampleName,
                                              self.confName,
                                              self.dataName,
                                              ' '.join(self.resultFiles))
        return out

    @staticmethod
    def dbTbl():
        return resultTbl()

    
################################################################################

class Conf(Record):
    def __init__(self, **kwargs):
        super(Conf, self).__init__(kwargs['name'])
        self.conf = kwargs['conf']

    def to_dict(self):
        out = {
            'name': self.name,
            'conf': self.conf
            }
        return out

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)
    
    @staticmethod
    def dbTbl():
        return confTbl()

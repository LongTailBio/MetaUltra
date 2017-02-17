from tinydb import TinyDB, Query, where
import meta_ultra.config as config
from meta_ultra.utils import *
from os.path import basename

db = TinyDB(config.db_file)
sampleTbl = db.table(config.db_sample_table)
dataTbl = db.table(config.db_data_table)
experimentTbl = db.table(config.db_experiment_table)
resultTbl = db.table(config.db_result_table)
confTbl = db.table(config.db_conf_table)

################################################################################
#
# Classes
#
################################################################################

class RecordExistsError(Exception):
    pass

class DataTypeNotFoundError(Exception):
    pass

def checkDataType(dataType):
    types = ['seq_single_ended',
             'seq_paired_ended']
    if dataType in types:
        return dataType
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
        return type(self).dbTbl().get(where('name') == self.name)

    def saved(self):
        return type(self).exists(self.name)
    
    def save(self,modify=False):
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
        

    @classmethod
    def build(ctype, *args, **kwargs):
        return ctype(**kwargs)

        
    @classmethod
    def get(ctype, name):
        rec = ctype.dbTbl().get(where('name') == name)
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
        self.dataType = checkDataType(dataType)
        self.sampleName = sampleName
        self.projectName = projectName
        self.experimentName = experimentName
        
    def to_dict(self):
        out = {
            'name': self.name,
            'data_type': self.dataType,
            'sample_name':self.sampleName,
            'project_name': self.projectName,
            'experiment_name':self.experimentName
            }
        self._to_dict(out)
        return out

    @staticmethod
    def dbTbl():
        return dataTbl

    @classmethod
    def build(ctype, *args, **kwargs):
        if kwargs['data_type'] == 'seq_single_ended':
            return SingleEndedSeqData(**kwargs)
        elif kwargs['data_type'] == 'seq_paired_ended':
            return PairedEndedSeqData(**kwargs)
        else:
            raise DataTypeNotFoundError()
    
class SingleEndedSeqData(Data):
    def __init__(self,**kwargs):
        super(SingleEndedSeqData, self).__init__(kwargs['name'],
                                                 'seq_single_ended',
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

    

class PairedEndedSeqData(Data):
    def __init__(self,**kwargs):
        super(PairedEndedSeqData, self).__init__(kwargs['name'],
                                                 'seq_paired_ended',
                                                 kwargs['sample_name'],
                                                 kwargs['project_name'],
                                                 kwargs['experiment_name'])
        self.reads1 = kwargs['reads_1']
        self.registerFile(self.reads1)
        self.reads2 = kwargs['reads_2']
        self.registerFile(self.reads2)
        self.aveReadLen = int(kwargs['ave_read_length'])
        self.aveGapLen = int(kwargs['ave_gap_length'])

    def _to_dict(self, out):
        out['reads_1'] = self.reads1
        out['reads_2'] = self.reads2
        out['ave_read_length'] = self.aveReadLen
        out['ave_gap_length'] = self.aveGapLen
        return out

    def __str__(self):
        out = '{}\t{}\t{}\t{}\t{}'.format(self.name, self.dataType,self.experimentName,self.reads1,self.reads2)
        return out


################################################################################

class Experiment(Record):
    def __init__(self, name, dataType):
        super(Experiment, self).__init__(name)
        self.dataType = checkDataType(dataType)

    def to_dict(self):
        out = {
            'name': self.name,
            'data_type': self.dataType
        }
        self._to_dict(out)
        return(out)

    @staticmethod
    def dbTbl():
        return experimentTbl

    
class SingleEndedSequencingRun( Experiment):
    def __init__(self,**kwargs):
        super(SingleEndedSequencingRun, self).__init__(kwargs['name'],
                                                       'seq_single_ended')
        self.machineType = kwargs['machine_type']

    def _to_dict(self,out):
        out['machine_type'] = self.machineType
        return out

class PairedEndedSequencingRun( Experiment):
    def __init__(self,**kwargs):
        super(PairedEndedSequencingRun, self).__init__(kwargs['name'],
                                                       'seq_paired_ended')
        self.machineType = kwargs['machine_type']

    def _to_dict(self,out):
        out['machine_type'] = self.machineType
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
        return sampleTbl

    
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
        return resultTbl

    
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
    
    @staticmethod
    def dbTbl():
        return confTbl

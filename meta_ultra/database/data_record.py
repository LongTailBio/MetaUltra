from .database import *
from .sample import *
from .project import *
from .experiment import *

dataTbl = config.db_data_table



class Data( Record):
    def __init__(self, name, dataType, sampleName, projectName, experimentName):
        super(Data, self).__init__(name)
        self.dataType = DataType.asDataType(dataType)
        self.sampleName = sampleName
        try:
            self.sampleType = SampleType.asSampleType(Sample.get(self.sampleName).sampleType)
        except NoSuchRecordError:
            raise InvalidRecordStateError()
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

    def __str__(self):
        out = '{}\t{}\t{}\t{}\t{}'.format(self.name,
                                    DataType.toString( self.dataType),
                                    self.sampleName,
                                    self.experimentName,
                                    self.projectName)
        return out
    
    @staticmethod
    def dbTbl():
        return dataTbl()

    @classmethod
    def build(ctype, *args, **kwargs):
        dataType = DataType.asDataType( kwargs['data_type'])
        if dataType == DataType.WGS_DNA_SEQ_SINGLE_END:
            return SingleEndDNASeqData(**kwargs)
        elif dataType == DataType.WGS_DNA_SEQ_PAIRED_END:
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
        try:
            self.metadata = kwargs['metadata']
        except KeyError:
            self.metadata = {}
        self.reads1 = kwargs['reads_1']
        self.registerFile(self.reads1)
        self.aveReadLen = int(kwargs['ave_read_length'])

    def _to_dict(self, out):
        out['metadata'] = self.metadata
        out['reads_1'] = self.reads1
        out['ave_read_length'] = self.aveReadLen
        return out

    @staticmethod
    def dataType():
        return DataType.WGS_DNA_SEQ_SINGLE_END


    
class PairedEndDNASeqData(Data):
    def __init__(self,**kwargs):
        super(PairedEndDNASeqData, self).__init__(kwargs['name'],
                                                  type(self).dataType(),
                                                  kwargs['sample_name'],
                                                 kwargs['project_name'],
                                                 kwargs['experiment_name'])
        try:
            self.metadata = kwargs['metadata']
        except KeyError:
            self.metadata = {}

        self.reads1 = kwargs['reads_1']
        self.registerFile(self.reads1)
        self.reads2 = kwargs['reads_2']
        self.registerFile(self.reads2)
        self.aveReadLen = int(kwargs['ave_read_length'])
        try:
            self.aveGapLen = int(kwargs['ave_gap_length'])
        except (TypeError, KeyError, ValueError):
            self.aveGapLen = None
            
    def _to_dict(self, out):
        out['metadata'] = self.metadata
        out['reads_1'] = self.reads1
        out['reads_2'] = self.reads2
        out['ave_read_length'] = self.aveReadLen
        out['ave_gap_length'] = self.aveGapLen
        return out


    @staticmethod
    def dataType():
        return DataType.WGS_DNA_SEQ_PAIRED_END



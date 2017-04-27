
from .database import *

experimentTbl = config.db_experiment_table

class Experiment(Record):
    def __init__(self, name, dataType):
        super(Experiment, self).__init__(name)
        self.dataType = DataType.asDataType(dataType)

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
        dataType = DataType.asDataType( kwargs['data_type'])
        if dataType == DataType.WGS_DNA_SEQ_SINGLE_END:
            return SingleEndDNASeqRun(**kwargs)
        elif dataType == DataType.WGS_DNA_SEQ_PAIRED_END:
            return PairedEndDNASeqRun(**kwargs)
        else:
            raise DataTypeNotFoundError()

    def __str__(self):
        out = '{}\t{}'.format(self.name,
                                    DataType.asString( self.dataType))
        return out

        
    
class SingleEndDNASeqRun( Experiment):
    def __init__(self,**kwargs):
        super(SingleEndDNASeqRun, self).__init__(kwargs['name'],
                                                       DataType.WGS_DNA_SEQ_SINGLE_END)
        self.metadata = kwargs['metadata']
        if not self.metadata:
            self.metadata = {}
            
    def _to_dict(self,out):
        out['metadata'] = self.metadata
        return out

class PairedEndDNASeqRun( Experiment):
    def __init__(self,**kwargs):
        super(PairedEndDNASeqRun, self).__init__(kwargs['name'],
                                                       DataType.WGS_DNA_SEQ_PAIRED_END)
        self.metadata = kwargs['metadata']
        if not self.metadata:
            self.metadata = {}

    def _to_dict(self,out):
        out['metadata'] = self.metadata
        return out


from .database import *
from .data_record import *
from .sample import *
from .project import *
from .experiment import *
resultTbl = config.db_result_table

class Result( BaseRecord):
    def __init__(self, **kwargs):
        super(Result, self).__init__(**kwargs)
        self._previousResults = kwargs['previous_results']
        self._fileRecords = kwargs['file_records']
        self.resultType = ResultType( kwargs['result_type'])

    def to_dict(self):
        out = super(Sample, self).to_dict()
        out['previous_results'] = self._previousResults
        out['file_records'] = self._fileRecords
        out['result_type'] = str( self.resultType)
        return out

    def files(self):
        raise NotImplementedError()
    
    def validStatus(self):
        raise NotImplementedError()        

    
    def __str__(self):
        out = '{}\t{}'.format(self.name,
                              self.moduleName,
                              self.resultType)
        return out

    @staticmethod
    def dbTbl():
        return resultTbl()


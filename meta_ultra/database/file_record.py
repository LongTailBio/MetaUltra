from .database import *
from .data_record import *
from .sample import *
from .project import *
from .experiment import *

fileRecordTbl = config.db_file_record_table

class FileRecord( BaseRecord):
    def __init__(self, **kwargs):
        super(Result, self).__init__(**kwargs)
        self.filepath = kwargs['filepath']
        self.format = FileFormat( kwargs['file_format'])        
        try:
            self.checksum = kwargs['checksum']
        except KeyError:
            self.checksum = self._currentChecksum()


    def to_dict(self):
        out = super(Sample, self).to_dict()
        out['filepath'] = self.filepath
        out['checksum'] = self.checksum
        out['file_format'] = str( self.format)
        return out

    def _currentChecksum(self):
        raise NotImplementedError()
    
    def validStatus(self):
        raise NotImplementedError()        

    
    def __str__(self):
        out = '{}\t{}'.format(self.checksum,
                              self.filepath)
        return out

    @staticmethod
    def dbTbl():
        return resultTbl()


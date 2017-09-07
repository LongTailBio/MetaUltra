from .database import *
from .data_record import *
from .sample import *
from .project import *
from .experiment import *
resultTbl = config.db_result_table

class Result(Record):
    def __init__(self, **kwargs):
        super(Result, self).__init__(kwargs['name'])
        self.projectName = kwargs['project_name']
        self.sampleName = kwargs['sample_name']
        self.experimentName = kwargs['experiment_name']
        self.dataName = kwargs['data_name']
        self.confName = kwargs['conf_name']
        self.moduleName = kwargs['module_name']
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
            'experiment_name':self.experimentName,
            'sample_name': self.sampleName,
            'data_name': self.dataName,
            'conf_name': self.confName,
            'result_files':self.resultFiles,
            'module_name':self.moduleName
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
        return self.status()

    
    def __str__(self):
        out = '{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(self.name,
                                                  self.moduleName,
                                                  self.projectName,
                                                  self.sampleName,
                                                  self.confName,
                                                  self.dataName,
                                                  ' '.join(self.resultFiles))
        return out

    @staticmethod
    def dbTbl():
        return resultTbl()


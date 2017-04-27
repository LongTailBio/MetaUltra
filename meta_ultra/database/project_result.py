from .database import *

projectResultTbl = config.db_project_result_table

class ProjectResult(Record):
    def __init__(self, **kwargs):
        super(Result, self).__init__(kwargs['name'])
        self.projectName = kwargs['project_name']
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
            'conf_name': self.confName,
            'result_files':self.resultFiles,
            'module_name':self.moduleName
            }
        return out

    def validStatus(self):
        try:
            Project.get(self.projectName)
        except NoSuchRecordError:
            return False
        return True

    
    def __str__(self):
        out = '{}\t{}\t{}\t{}'.format(self.name,
                                              self.projectName,
                                              self.confName,
                                              ' '.join(self.resultFiles))
        return out

    @staticmethod
    def dbTbl():
        return projectResultTbl()


from .database import *

projectTbl = config.db_project_table
        
class Project(Record):
    def __init__(self,**kwargs):
        super(Project, self).__init__(kwargs['name'])
        if 'metadata' in kwargs and kwargs['metadata']:
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

    
    

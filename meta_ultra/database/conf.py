from .database import *

confTbl = config.db_conf_table

class Conf(Record):
    def __init__(self, **kwargs):
        super(Conf, self).__init__(kwargs['name'])
        self.confDict = kwargs['conf_dict']

    def to_dict(self):
        out = {
            'name': self.name,
            'conf_dict': self.confDict
            }
        return out

    def __str__(self):
        return self.name
    
    @staticmethod
    def dbTbl():
        return confTbl()

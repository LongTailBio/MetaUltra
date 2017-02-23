from .api_utils import *
import meta_ultra.config as config
from meta_ultra.database import *
import os.path
import os
    
def removeData(name, atomic=False):
    if atomic:
        Data.get(name).remove()
    else:
        raise NotImplementedError()

def removeProject(name, atomic=False):
    if atomic:
        Project.get(name).remove()
    else:
        raise NotImplementedError()

def removeExperiment(name, atomic=False):
    if atomic:
        Experiment.get(name).remove()
    else:
        raise NotImplementedError()

def removeSample(name, atomic=False):
    if atomic:
        Sample.get(name).remove()
    else:
        raise NotImplementedError()
    

def removeResult(name, atomic=False):
    if atomic:
        Result.get(name).remove()
    else:
        raise NotImplementedError()
        



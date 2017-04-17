from .api_utils import *
import meta_ultra.config as config
from meta_ultra.database import *
from .getters import *
import os.path
import os
    
def removeData(name, atomic=False):
    if type(name) != str:
        name = name.name
    if atomic:
        Data.get(name).remove()
    else:
        results = getResults(dataRecs=[name])
        for result in results:
            removeResult(result)
        Data.get(name).remove()
        
def removeConf(name, atomic=False):
    if type(name) != str:
        name = name.name
    if atomic:
        Conf.get(name).remove()
    else:
        results = getResults(confs=[name])
        for result in results:
            removeResult(result)
        Conf.get(name).remove()
            
def removeProject(name, atomic=False):
    if type(name) != str:
        name = name.name
    if atomic:
        Project.get(name).remove()
    else:
        samples = getSamples(projects=[name])
        for sample in samples:
            removeSample(sample)
        Project.get(name).remove()

def removeExperiment(name, atomic=False):
    if type(name) != str:
        name = name.name
    if atomic:
        Experiment.get(name).remove()
    else:
        dataRecs = getData(experiments=[name])
        for dataRec in dataRecs:
            removeData(dataRec)
        Experiment.get(name).remove()

def removeSample(name, atomic=False):
    if type(name) != str:
        name = name.name
    if atomic:
        Sample.get(name).remove()
    else:
        dataRecs = getData(samples=[name])
        for dataRec in dataRecs:
            removeData(dataRec)
        Sample.get(name).remove()

    
def removeResult(name, atomic=False):
    if type(name) != str:
        name = name.name
    Result.get(name).remove()

def removeProjectResult(name, atomic=False):
    if type(name) != str:
        name = name.name
    ProjectResult.get(name).remove()




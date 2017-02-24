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

def removeProject(name, atomic=False):
    if type(name) != str:
        name = name.name
    if atomic:
        Project.get(name).remove()
    else:
        samples = getSamples(projects=[name])
        for sample in samples:
            removeSample(sample)

def removeExperiment(name, atomic=False):
    if type(name) != str:
        name = name.name
    if atomic:
        Experiment.get(name).remove()
    else:
        dataRecs = getData(experiments=[name])
        for dataRec in dataRecs:
            removeData(dataRec)

def removeSample(name, atomic=False):
    if type(name) != str:
        name = name.name
    if atomic:
        Sample.get(name).remove()
    else:
        dataRecs = getData(samples=[name])
        for dataRec in dataRecs:
            removeData(dataRec)


    
def removeResult(name, atomic=False):
    if type(name) != name:
        name = name.name
    Result.get(name).remove()
            



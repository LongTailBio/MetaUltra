from .api_utils import *
import meta_ultra.config as config
from meta_ultra.database import *
import os.path
import os
    
def removeData(name):
    Data.get(name).remove()

def removeProject(name):
    Project.get(name).remove()

def removeExperiment(name):
    Experiment.get(name).remove()

def removeSample(name):
    Sample.get(name).remove()

def removeResult(name):
    Result.get(name).remove()



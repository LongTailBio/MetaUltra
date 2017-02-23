from .api_utils import *
import meta_ultra.config as config
from meta_ultra.database import *
import os.path
import os
    

################################################################################
#
# Info Retrieval
#
################################################################################

def getProject(name):
    return Project.get(name)

def getProjects(names=None):
    if not names or len(names) == 0:
        return Project.all()
    else:
        return [getProject(name) for name in names]

############################################################

def getExperiment(name):
    return experiment.get(name)

def getExperiments(dataTypes=None):
    dataTypes = convertDataTypes(dataTypes)
    out = []
    for exp in Experiment.all():
        if exp.dataType in dataTypes:
            out.append(exp)
    return out

############################################################

def getConf(name):
    return Conf.get(name)

def getConfs(names=None):
    if not names or len(names) == 0:
        Conf.all()
    else:
        return [getConf(name) for name in names]

###########################################################

def getSample(name):
    raise NotImplementedError


def getSampleTypes():
    raise NotImplementedError

def getSamples(projects=None):
    projNames = toNameList(projects)
    samples = Sample.all()
    out = []
    for sample in samples:
        if len(projNames) == 0 or sample.projectName in projNames:
            out.append(sample)
    return out

###########################################################

def getDataTypes():
    raise NotImplementedError

def getDataRec(name):
    return Data.get(name)

def getData(names=None, dataTypes=None, samples=None, experiments=None, projects=None):
    sampleNames = toNameList(samples)
    expNames = toNameList(experiments)
    projNames = toNameList(projects)
    dataTypes = convertDataTypes(dataTypes)
    dataRecs = Data.all()
    out = []
    for dataRec in dataRecs:
        if ( ( len(dataTypes) == 0 or dataRec.dataType in dataTypes)
             and (len(expNames) == 0 or dataRec.experimentName in expNames)
             and (len(projNames) == 0 or dataRec.projectName in projNames)
             and (len(sampleNames) == 0 or dataRec.sampleName in sampleNames)):
            out.append(dataRec)
    return out

def getSingleEndedSeqData(samples=None, experiments=None, projects=None):
    return getData(SingleEndedSeqData.dataType(),
                   samples=samples,
                   experiments=experiments,
                   projects=projects
                   )

def getPairedEndedSeqData(samples=None, experiments=None, projects=None):
    return getData(PairedEndedSeqData.dataType(),
                   samples=samples,
                   experiments=experiments,
                   projects=projects
                   )

def getResults(names=None, dataTypes=None, samples=None, experiments=None, projects=None, dataRecs=None, confs=None):
    sampleNames = toNameList(samples)
    expNames = toNameList(experiments)
    projNames = toNameList(projects)
    dataRecs = toNameList(dataRecs)
    confs = toNameList(confs)
    dataTypes = convertDataTypes(dataTypes)
    results = Result.all()
    out = []
    for  result in results:
        dataRec = getDataRec(result.dataName)
        if ( (len(dataRecs) == 0 or dataRec.name in dataRecs)
             and (len(dataTypes) == 0  or dataRec.dataType in dataTypes)
             and (len(confs) == 0 or result.confName in confs)
             and (len(expNames) == 0 or dataRec.experimentName in expNames)
             and (len(projNames) == 0 or dataRec.projectName in projNames)
             and (len(sampleNames) == 0 or dataRec.sampleName in sampleNames)):
            out.append(result)
    return out


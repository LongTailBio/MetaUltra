from .api_utils import *
import meta_ultra.config as config
from meta_ultra.database import *
from meta_ultra.data_type import *
from meta_ultra.sample_type import *
import meta_ultra.modules as modules
import os.path
import os
    

################################################################################
#
# Info Retrieval
#
################################################################################

def getProject(name):
    try:
        return Project.get(name)
    except NoSuchRecordError:
        return None

def getProjects(names=None):
    if not names or len(names) == 0:
        return Project.all()
    else:
        return [getProject(name) for name in names]

############################################################

def getExperiment(name):
    try:
        return Experiment.get(name)
    except NoSuchRecordError:
        return None

def getExperiments(names=None, dataTypes=None, dataRecs=None):
    dataTypes = convertDataTypes(dataTypes)

    if dataRecs and len(dataRecs) > 0:
        expsInDataRecs = [dR.experimentName for dR in getData(names=dataRecs)]
        expsInDataRecs = set(expsInDataRecs)
    else:
        expsInDataRecs = None
        
    out = []
    for exp in Experiment.all():
        if( (not names or len(names) == 0 or exp.name in names)
            and (len(dataTypes) == 0 or exp.dataType in dataTypes)):
            if not expsInDataRecs or exp.name in expsInDataRecs:
                out.append(exp)
    return out

############################################################

def getConf(name):
    try:
        return Conf.get(name)
    except NoSuchRecordError:
        return None

def getConfs(names=None):
    if not names or len(names) == 0:
        confs = Conf.all()
    else:
        confs = [getConf(name) for name in names]
    return confs
    

###########################################################

def getSampleTypes():
    return SampleType

def getSample(name):
    try:
        return Sample.get(name)
    except NoSuchRecordError:
        return None

def getSamples(projects=None, names=None):
    projNames = toNameList(projects)
    samples = Sample.all()
    out = []
    for sample in samples:
        if( (not names or len(names) == 0 or sample.name in names)
            and (len(projNames) == 0 or sample.projectName in projNames)):
            out.append(sample)
    return out

###########################################################

def getDataTypes():
    return DataType

def getDataRec(name):
    try:
        return Data.get(name)
    except NoSuchRecordError:
        return None

def getData(names=None, dataTypes=None, samples=None, experiments=None, projects=None):
    sampleNames = toNameList(samples)
    expNames = toNameList(experiments)
    projNames = toNameList(projects)
    dataTypes = convertDataTypes(dataTypes)
    dataRecs = Data.all()
    out = []
    for dataRec in dataRecs:
        if ( (not names or len(names) == 0 or dataRec.name in names)
             and (len(dataTypes) == 0 or dataRec.dataType in dataTypes)
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

def getResult(name):
    try:
        return Result.get(name)
    except NoSuchRecordError:
        return None

def getResults(names=None,
               dataTypes=None,
               samples=None,
               experiments=None,
               projects=None,
               dataRecs=None,
               confs=None,
               modules=None):
    names = toNameList(names)
    sampleNames = toNameList(samples)
    expNames = toNameList(experiments)
    projNames = toNameList(projects)
    dataRecs = toNameList(dataRecs)
    confs = toNameList(confs)
    dataTypes = convertDataTypes(dataTypes)
    modules = toNameList(modules)
    query = Query()
    if len(projNames) == 1: # hack to test something...
        results = Result.search(query.project_name == projNames[0])
    else:
        results = Result.all()
    out = []
    for  result in results:
        dataRec = getDataRec(result.dataName)
        if ( (len(dataRecs) == 0 or dataRec.name in dataRecs)
             and (len(dataTypes) == 0  or dataRec.dataType in dataTypes)
             and (len(confs) == 0 or result.confName in confs)
             and (len(expNames) == 0 or dataRec.experimentName in expNames)
             and (len(projNames) == 0 or dataRec.projectName in projNames)
             and (len(sampleNames) == 0 or dataRec.sampleName in sampleNames)
             and (len(names) == 0 or result.name in names)
             and ( len(modules) == 0 or result.moduleName in modules)):
            out.append(result)
#            print(result)
    return out


def getProjectResult(name):
    try:
        return ProjectResult.get(name)
    except NoSuchRecordError:
        return None

def getProjectResults(names=None, projects=None, confs=None):
    projNames = toNameList(projects)
    confs = toNameList(confs)
    projResults = ProjectResult.all()
    out = []
    for  pResult in projResults:
        if ( (len(confs) == 0 or pResult.confName in conf)
             and (len(projNames) == 0 or pResult.projectName in projNames)
             and (len(names) == 0 or pResult.name in names)):
            out.append(pResult)
    return out




def getModules(names=None):
    out = []
    for moduleType in modules.modules:
        if not names or len(names) == 0  or module.moduleName() in names:
            out.append( moduleType.build())
    return out

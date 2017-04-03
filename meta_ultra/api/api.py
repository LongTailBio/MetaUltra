import meta_ultra.config as config
from meta_ultra.database import *
import os.path
import os
from snakemake import snakemake
from .api_utils import *
from tinydb import where
import metagenscope_api as mgs_api
from .getters import *
from .savers  import *
from json import dumps as jdumps
from tempfile import NamedTemporaryFile
################################################################################
#
# Start a working area
#
################################################################################

def init(dir='.'):
    muDir = os.path.join(dir, config.mu_dir)
    os.makedirs(muDir)

################################################################################
#
# Run modules
#
################################################################################

def runModules(confWithData,dataRecs,jobs,dryrun=False,unlock=False,rerun=False):
    with open(config.snakemake_static_conf_file(), 'w') as snkConf:
        snkConf.write( jdumps(confWithData))
    snakemake(config.snake_file,
                     config=confWithData,
                     cluster=config.cluster_wrapper,
                     keepgoing=True,
                     printshellcmds=True,
                     dryrun=dryrun,
                     unlock=unlock,
                     force_incomplete=rerun,
                     nodes=jobs)
    
################################################################################
#
# Sync with metagenscope
#
################################################################################

def getRemotes():
    muRemotes = config.db_mu_config_remotes()
    out = {}
    for remoteRec in muRemotes.all():
        out[remoteRec['name']] = remoteRec['url']
    return out

def getRemoteURL(remoteName):
    remoteName = remoteName.strip().lower()
    muRemotes = config.db_mu_config_remotes()
    if muRemotes.contains(where('name') == remoteName):
        return muRemotes.get(where('name') == remoteName)['url']
    return None

def addRemote(remoteName, remoteURL):
    remoteName = remoteName.strip().lower()
    muRemotes = config.db_mu_config_remotes()
    if getRemoteURL(remoteName):
        return False
    muRemotes.insert({'name':remoteName, 'url':remoteURL})
    return getRemoteURL(remoteName)

def editRemote(remoteName, remoteURL):
    remoteName = remoteName.strip().lower()
    muRemotes = config.db_mu_config_remotes()
    if muRemotes.contains(where('name') == remoteName):
        remote = muRemotes.get(where('name') == remoteName)
        return muRemotes.update({'url':remoteURL}, eids=[remote.eid])

def removeRemote(remoteName):
    remoteName = remoteName.strip().lower()
    muRemotes = config.db_mu_config_remotes()
    if muRemotes.contains(where('name') == remoteName):
        remote = muRemotes.get(where('name') == remoteName)
        return muRemotes.remove(eids=[remote.eid])

def syncOverwrite(remoteName, projects=[]):
    remoteURL = getRemoteURL(remoteName)
    uploader = mgs_api.Uploader(remoteURL)

    successfulProjects = []
    for project in getProjects(names=projects):
        result = uploader.new_project(project.name,
                                      metadata=project.metadata,
                                      overwrite=True)
        if result:
            successfulProjects.append(project)
            yield True, project
        else:
            yield False, project


            
    successfulSamples = []
    for sample in getSamples(projects=successfulProjects):
        if not sample.validStatus():
            continue
        result = uploader.new_sample(sample.name,
                                     sample.projectName,
                                     SampleType.asString(sample.sampleType),
                                     metadata=sample.metadata,
                                     overwrite=True)
        if result:
            successfulSamples.append(sample)
            yield True, sample
        else:
            yield False, sample


    successfulExps = []
    for exp in getExperiments():
        result = uploader.new_experiment(exp.name,
                                         DataType.asString(exp.dataType),
                                         metadata=exp.metadata,
                                         overwrite=True)
        if result:
            successfulExps.append(exp)
            yield True, exp
        else:
            yield False, exp
            

    
    successfulData = []
    for dataRec in getData(projects=successfulProjects,
                           experiments=successfulExps,
                           samples=successfulSamples):

        result = uploader.new_data_record(dataRec.name,
                                          dataRec.sampleName,
                                          dataRec.experimentName,
                                          DataType.asString(dataRec.dataType),
                                          metadata=dataRec.metadata,
                                          overwrite=True)
        if result:
            successfulData.append( dataRec)
            yield True, dataRec
        else:
            yield False, dataRec

    for result in getResults(dataRecs=successfulData):
        try:
            upResult = uploader.new_result(result.name,
                                       result.dataName,
                                       result.moduleName,
                                       filenames=result.resultFiles,
                                       overwrite=True)
        except:
            yield False, result

        if upResult:
            yield True, result
        else:
            yield False, result
                                     
    

    
    

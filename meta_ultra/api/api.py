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
    try:
        os.makedirs( config.mu_config_dir)
    except FileExistsError:
        pass
    muDir = os.path.join(dir, config.mu_repo_dir)
    try:
        os.makedirs(muDir)
    except FileExistsError:
        pass

################################################################################
#
# Run modules
#
################################################################################

def runModules(confWithData,dataRecs,jobs,dryrun=False,unlock=False,rerun=False):
    with open(config.snakemake_static_conf_file(), 'w') as snkConf:
        snkConf.write( jdumps(confWithData))
    snakemake(config.snake_file(),
                     config=confWithData,
                     cluster=config.cluster_wrapper(),
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

def syncOverwrite(remoteName, projects=[], resultsOnly=False, resultType=None):
    remoteURL = getRemoteURL(remoteName)
    uploader = mgs_api.Uploader(remoteURL)

    if not resultsOnly:
        successfulProjects = []
        for project in getProjects(names=projects):
            success, response = uploader.new_project(project.name,
                                          metadata=project.metadata,
                                          overwrite=True)
            if success:
                successfulProjects.append(project)
                yield True, project, response
            else:
                yield False, project, response


            
        successfulSamples = []
        for sample in getSamples(projects=successfulProjects):
            if not sample.validStatus():
                continue
            success, response = uploader.new_sample(sample.name,
                                         sample.projectName,
                                         SampleType.asString(sample.sampleType),
                                         metadata=sample.metadata,
                                         overwrite=True)
            if success:
                successfulSamples.append(sample)
                yield True, sample, response
            else:
                yield False, sample, response


        successfulExps = []
        for exp in getExperiments():
            success, response = uploader.new_experiment(exp.name,
                                             DataType.asString(exp.dataType),
                                             metadata=exp.metadata,
                                             overwrite=True)
            if success:
                successfulExps.append(exp)
                yield True, exp, response
            else:
                yield False, exp, response
            

    
        successfulData = []
        for dataRec in getData(projects=successfulProjects,
                               experiments=successfulExps,
                               samples=successfulSamples):

            success, response = uploader.new_data_record(dataRec.name,
                                              dataRec.sampleName,
                                              dataRec.experimentName,
                                              DataType.asString(dataRec.dataType),
                                              metadata=dataRec.metadata,
                                              overwrite=True)
            if success:
                successfulData.append( dataRec)
                yield True, dataRec, response
            else:
                yield False, dataRec, response

    if resultsOnly:
        successfulData = []
    
    for result in getResults(dataRecs=successfulData, modules=[resultType]):
        success = False
        try:
            rFiles = result.resultFiles
            if result.moduleName == 'humann2':
                rFiles = [el for el in rFiles if 'coverage' in el or 'abundance' in el]
            success, response = uploader.new_result(result.name,
                                           result.dataName,
                                           result.moduleName,
                                           filenames=rFiles,
                                           overwrite=True)
        except Exception as e:
            print(e, file=sys.stderr)
            yield False, result, None
            

        if success:
            yield True, result, response
        else:
            yield False, result, response
                                     
    

    
    

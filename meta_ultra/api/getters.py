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
# Get records from the repo
#
################################################################################

def _genericSingleGetter(ctype, name, repo):
    name = toName(name)
    try:
        return ctype.get(name, repo=repo)
    except NoSuchRecordError:
        return None

def _genericMultiGetter(ctype, names, repo):
    closeRepo = False
    if repo is None:
        repo = Repo.getRepo()
        closeRepo = True
    names = toNameSet(names)
    if not names or len(names) == 0:
        datums = ctype.all(repo=repo)
    else:
        datums = [_genericSingleGetter(ctype, name, repo) for name in names]
    if closeRepo:
        repo.close()
    return datums

###########################################################

def getSampleGroup(name, repo=None):
    return _genericSingleGetter(SampleGroup, name, repo)

def getSampleGroups(names=None, repo=None):
    return _genericMultiGetter(SampleGroup, names, repo)
    
def getSampleTypes():
    return SampleType

def getSample(name, repo=None):
    return _genericSingleGetter( Sample, name, repo)

def getSamples(sampleGroups=None, names=None, repo=None):
    groups = getSampleGroups(names=sampleGroups, repo=repo)
    names = toNameSet(names)
    for group in groups
        for sample in group.samples():
            names.add( sample.name)

    return _genericMultiGetter( Sample, names, repo)

###########################################################

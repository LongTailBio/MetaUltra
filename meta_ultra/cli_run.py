from meta_ultra.user_input import *
import meta_ultra.cli_add as add
import meta_ultra.api as api


################################################################################

def run(dryrun=False, unlock=False, rerunIncomplete=False):
    conf = UserChoice('conf', api.getConfs(), new=add.addConf()).resolve()
    dataType = UserChoice('Select data type to analyze',
                          api.getDataTypes()).resolve()
    projects = None
    if BoolUserInput('Select data from a specific project?'.format(name),
                     False).resolve():
        projects = UserMultiChoice('What projects should data be taken from',
                             api.getProjects()).resolve()
    samples=None
    if BoolUserInput('Select data from a specific samples?'.format(name),
                     False).resolve():
        samples = UserMultiChoice('What samples should data be taken from?',
                                  api.getSamples(projects=projects)).resolve()
    dataRecs = getData(dataType=dataType, projects=projects,samples=samples)
    api.runModules(conf,dataRecs,dryrun=dryrun, unlock=unlock, rerun=rerunIncomplete)


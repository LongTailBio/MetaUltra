from meta_ultra.user_input import *
from .cli_add import *
import meta_ultra.api as api
from .cli import main
import click

################################################################################

@main.command()
@click.option('--dryrun/--wetrun',default=False,help='Show what result files would be built')
@click.option('--unlock/--locked',default=False,help='Unlock the working directory')
@click.option('--rerun/--no-rerun',default=False,help='Rebuild files that might be incomplete')
def run(dryrun=False, unlock=False, rerunIncomplete=False):
    conf = UserChoice('conf', api.getConfs(), new=addConf()).resolve()
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


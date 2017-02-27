from meta_ultra.user_input import *
from .cli_add import *
import meta_ultra.api as api
from .cli import main
import click
import meta_ultra.conf_builder as conf_builder

################################################################################

@main.command()
@click.option('--jobs',default=1,help='How many jobs should be run simultaneously?')
@click.option('--dryrun/--wetrun',default=False,help='Show what result files would be built')
@click.option('--unlock/--locked',default=False,help='Unlock the working directory')
@click.option('--rerun/--no-rerun',default=False,help='Rebuild files that might be incomplete')
def run(jobs, dryrun=False, unlock=False, rerun=False):

    conf = UserChoice('conf', api.getConfs(), new=addConf).resolve()

    projects = None
    if BoolUserInput('Select data from specific projects?', False).resolve():
        projects = UserMultiChoice('What projects should data be taken from',
                             api.getProjects()).resolve()
    samples=None
    if BoolUserInput('Select data from a specific samples?', False).resolve():
        samples = UserMultiChoice('What samples should data be taken from?',
                                  api.getSamples(projects=projects)).resolve()
    dataRecs = api.getData(projects=projects,samples=samples)

    confName = conf.name
    confWithData = conf_builder.addSamplesToConf(confName, dataRecs)              

    api.runModules(confWithData,dataRecs,jobs, dryrun=dryrun, unlock=unlock, rerun=rerun)


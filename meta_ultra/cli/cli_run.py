from meta_ultra.user_input import *
from .cli_add import *
import meta_ultra.api as api
from .cli import main
import click
import meta_ultra.conf_builder as conf_builder

################################################################################

@main.command()
@click.option('--jobs',default=1,type=int, help='How many jobs should be run simultaneously?')
@click.option('--choose/--all',default=False,help='Choose specific samples, projects, or experiments to process')
@click.option('--local/--on-cluster',default=False,help='Run jobs locally')
@click.option('--conf',default=None,type=str, help='Conf to use')
@click.option('--dryrun/--wetrun',default=False,help='Show what result files would be built')
@click.option('--unlock/--locked',default=False,help='Unlock the working directory')
@click.option('--rerun/--no-rerun',default=False,help='Rebuild files that might be incomplete')
@click.option('--results',default=None,type=str, help='Directory for output')
@click.option('--clean',default=None,type=str, multiple=True, help='Clean metadata of given file')
def run( jobs, choose, local=False, conf=None, dryrun=False, unlock=False, rerun=False, results=None, clean=None):
    if not conf:
        conf = UserChoice('conf', api.getConfs(), new=addConf).resolve()
    
    projects = None
    if choose and BoolUserInput('Select data from specific projects?', False).resolve():
        projects = UserMultiChoice('What projects should data be taken from',
                             api.getProjects()).resolve()
    samples=None
    if choose and BoolUserInput('Select data from a specific samples?', False).resolve():
        samples = UserMultiChoice('What samples should data be taken from?',
                                  api.getSamples(projects=projects)).resolve()

    experiments=None
    if choose and BoolUserInput('Select data from a specific experiments?', False).resolve():
        experiments = UserMultiChoice('What experiments should data be taken from?',
                                  api.getExperiments()).resolve()
        
    dataRecs = api.getData(projects=projects,samples=samples, experiments=experiments)

    confName = conf
    if type(conf) != str:
        confName = conf.name

    confWithData = conf_builder.addSamplesToConf(confName, dataRecs, outDir=results)              

    api.runModules(confWithData,
                   dataRecs,
                   jobs,
                   dryrun=dryrun,
                   local=local,
                   unlock=unlock,
                   rerun=rerun,
                   cleanMetadata=clean)


from meta_ultra.user_input import *
import meta_ultra.api as api
from meta_ultra.cli_colors import *
from .cli import main
import click

################################################################################

@main.command()
@click.option('--overwrite/--no-overwrite', default=False, help='Overwrite any matching data on the server')
@click.option('--results/--all', default=False, help='Only sync results, not objects')
@click.option('-m','--module',default=None, help='Only sync results from a given module')
@click.argument('remote',nargs=1)
@click.argument('projects', nargs=-1)
def sync(remote, projects, overwrite=False, results=False, module=None):
    if overwrite:
        for success, obj, response  in api.syncOverwrite(remote,
                                                projects=projects,
                                                resultsOnly=results,
                                                resultType=module):
            objType = type(obj)
            objType = objType.__name__
            objType = objType.split('.')[-1]
            if success:
                sys.stdout.write( cols.OKGREEN+ '{} {}: OK\n'.format(objType, obj.name) + cols.ENDC)
            else:
                sys.stdout.write(cols.FAIL+'{} {}: FAILED\n'.format( objType, obj.name) +  cols.ENDC)
                sys.stderr.write('{}\n'.format(response))
    else:
        raise NotImplementedError()

    

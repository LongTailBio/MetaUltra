from meta_ultra.user_input import *
import meta_ultra.api as api
from meta_ultra.cli_colors import *
from .cli import main
import click

################################################################################

@main.command()
@click.option('--overwrite/--no-overwrite', default=False, help='Overwrite any matching data on the server')
@click.argument('remote',nargs=1)
@click.argument('projects', nargs=-1)
def sync(remote, projects, overwrite=False):
    if overwrite:
        for success, obj in api.syncOverwrite(remote, projects=projects):
            objType = type(obj).__name__.split('.')[-1]
            if success:
                sys.stdout.write( cols.OKGREEN+ '{} {}: OK\n'.format(objType, obj.name) + cols.ENDC)
            else:
                sys.stdout.write(cols.FAIL+'{} {}: FAILED\n'.format( objType, obj.name) +  cols.ENDC)
                
    else:
        raise NotImplementedError()

    

from meta_ultra.user_input import *
import meta_ultra.api as api
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
            if success:
                sys.stdout.write('{}:\tOK\n'.format(obj))
            else:
                sys.stdout.write('{}:\tFAILED\n'.format(obj))
                
    else:
        raise NotImplementedError()

    

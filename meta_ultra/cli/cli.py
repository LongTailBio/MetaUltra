import os
import click

import meta_ultra.api as api


version = {}
version_path = os.path.join(os.path.dirname(__file__), '../version.py')
with open(version_path) as version_file:
    exec(version_file.read(), version)


@click.group()
@click.version_option(version['__version__'])
def main():
    pass

@main.command()
def init():
    api.init()

@main.group()
def config():
    pass

@config.command(name='remote')
def configRemote():
    raise NotImplementedError()
    
####################################################################################################
        
if __name__ == "__main__":
    main()

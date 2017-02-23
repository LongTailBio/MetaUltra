import click
import meta_ultra.api as api

@click.group()
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

from meta_ultra.user_input import *
import meta_ultra.api as api
from .cli import main
import click

@main.group()
def remove():
    pass


@remove.command(name='data')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.option('--atomic/--not-atomic',default=False,help='do not remove children')
@click.argument('names',nargs=-1)
def removeDataRecs(names, check=True, atomic=False):
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove data record {}?'.format(name),False).resolve()
        if remove:
            api.removeData(name, atomic=atomic)

            
@remove.command(name='projects')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.option('--atomic/--not-atomic',default=False,help='do not remove children')
@click.argument('names',nargs=-1)
def removeProjects(names, check=True, atomic=False):
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove project {}?'.format(name),False).resolve()
        if remove:
            api.removeProject(name, atomic=atomic)

@remove.command(name='confs')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.argument('names',nargs=-1)
def removeConfs(names, check=True):
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove conf {}?'.format(name),False).resolve()
        if remove:
            api.removeConf(name)

            
@remove.command(name='experiments')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.option('--atomic/--not-atomic',default=False,help='do not remove children')
@click.argument('names',nargs=-1)
def removeExperiments(names, check=True, atomic=False):
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove experiment {}?'.format(name),False).resolve()
        if remove:
            api.removeExperiment(name, atomic=atomic)


@remove.command(name='samples')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.option('--atomic/--not-atomic',default=False,help='do not remove children')
@click.argument('names',nargs=-1)
def removeSamples(names, check=True, atomic=False):
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove sample {}?'.format(name),False).resolve()
        if remove:
            api.removeSample(name, atomic=atomic)

            
@remove.command(name='results')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.option('--atomic/--not-atomic',default=False,help='do not remove children')
@click.option('--all/--not-all',default=False,help='remove all')
@click.argument('names',nargs=-1)
def removeResults(names=None, check=True, atomic=False, all=False):
    if all:
        names = [result.name for result in api.getResults()]
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove result {}?'.format(name),False).resolve()
        if remove:
            api.removeResult(name, atomic=atomic)


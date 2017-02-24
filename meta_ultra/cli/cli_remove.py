from meta_ultra.user_input import *
import meta_ultra.api as api
from .cli import main
import click

@main.group()
def remove():
    pass


@remove.command(name='data')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.argument('names',nargs=-1)
def removeDataRecs(names, check=True):
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove data record {}?'.format(name),False).resolve()
        if remove:
            results = api.getResults(dataRecs=[name])
            api.removeData(name)

            
@remove.command(name='projects')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.argument('names',nargs=-1)
def removeProjects(names, check=True):
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove project {}?'.format(name),False).resolve()
        if remove:
            samples = api.getSamples(projects=[name])
            api.removeProject(name)

@remove.command(name='experiments')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.argument('names',nargs=-1)
def removeExperiments(names, check=True):
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove experiment {}?'.format(name),False).resolve()
        if remove:
            dataRecs = api.getData(experiments=[name])
            api.removeExperiment(name)


@remove.command(name='samples')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.argument('names',nargs=-1)
def removeSamples(names, check=True):
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove sample {}?'.format(name),False).resolve()
        if remove:
            dataRecs = api.getData(samples=[name])
            api.removeSample(name)

            
@remove.command(name='results')
@click.option('--check/--no-check',default=True,help='ask before removing')
@click.argument('names',nargs=-1)
def removeResults(names=None, check=True):
    for name in names:
        remove = True
        if check:
            remove = BoolUserInput('Remove result {}?'.format(name),False).resolve()
        if remove:
            api.removeResult(name)


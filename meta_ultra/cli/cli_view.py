from meta_ultra.user_input import *
import meta_ultra.api as api
from .cli import main
import click

@main.group()
def view():
    pass

@view.command(name='projects')
@click.option('--tree/--list',default=False, help='Show as a tree')
@click.argument('names',nargs=-1)
def viewProjects(names, tree=False):
    if tree:
        raise NotImplementedError()
    else:
        for project in api.getProjects(names=names):
            print(project)

@view.command(name='confs')
@click.option('--tree/--list',default=False, help='Show as a tree')
@click.argument('names',nargs=-1)
def viewConfs(names, tree=False):
    if tree:
        raise NotImplementedError()
    else:
        for conf in api.getConfs(names=names):
            print(conf)

            
@view.command(name='samples')
@click.option('--tree/--list',default=False, help='Show as a tree')
@click.option('-p','--project',default=None, help='Show only samples from the given project')
@click.argument('names',nargs=-1)
def viewSamples(names, tree=False, project=None):
    if tree:
        raise NotImplementedError()
    else:
        for sample in api.getSamples(names=names, projects=[project]):
            print(sample)



@view.command(name='experiments')
@click.option('--tree/--list',default=False, help='Show as a tree')
@click.option('-t','--type',default=None, help='Only show data of a given type')
@click.argument('names',nargs=-1)
def viewExperiments(names, tree=False,type=None):
    if tree:
        raise NotImplementedError()
    else:
        for experiment in api.getExperiments(names=names, dataTypes=[type]):
            print(experiment)



@view.command(name='data')
@click.option('--tree/--list',default=False, help='Show as a tree')
@click.option('-t','--type',default=None, help='Only show data of a given type')
@click.option('-p','--project',default=None, help='Only show data from the given project')
@click.option('-s','--sample',default=None, help='Only show data from the given sample')
@click.argument('names',nargs=-1)
def viewData(names, tree=False, type=None, project=None, sample=None):
    if tree:
        raise NotImplementedError()
    else:
        for dataRec in api.getData(names=names, dataTypes=[type], projects=[project], samples=[sample]):
            print(dataRec)

@view.command(name='result')
@click.option('-t','--type',default=None, help='Only show results from data of a given type')
@click.option('-p','--project',default=None, help='Only show results from the given project')
@click.option('-s','--sample',default=None, help='Only show results from the given sample')
@click.option('-d','--data',default=None, help='Only show results from the given data record')
@click.option('-c','--conf',default=None, help='Only show results from the given conf')
@click.argument('names',nargs=-1)
def viewResults(names, type=None, project=None, sample=None, data=None, conf=None):
    for result in api.getResults(names=names,
                                 dataTypes=[type],
                                 projects=[project],
                                 samples=[sample],
                                 dataRecs=[data],
                                 confs=[conf]):
        print(result)


            

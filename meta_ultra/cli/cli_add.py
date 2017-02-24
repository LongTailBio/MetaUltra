from meta_ultra.user_input import *
import meta_ultra.api as api
from .cli import main
import click

@main.group()
def add():
    pass

@add.command(name='data')
@click.argument('filenames',nargs=-1)
def cli_addData(filenames):
    addData(filenames)
    
def addData(filenames):
    project = UserChoice('project', api.getProjects(), new=addProject).resolve()
    sampleType = UserChoice('sample_type', api.getSampleTypes()).resolve()
    dataType = UserChoice('data_type', api.getDataTypes()).resolve()
    if dataType == api.getDataTypes().DNA_SEQ_SINGLE_END:
        seqRun = UserChoice('sequencer_type', api.getExperiments(dataType=dataType),
                            new=lambda : addExperiment(dataType=dataType)).resolve()
        extension = UserInput('Please enter the file extension for the read files', '.fastq.gz').resolve()
        prefix = UserInput('Optionally, indicate a prefix for the read files', '').resolve()
        aveReadLen = UserInput('What is the average read length', type=int).resolve()
        api.bulkSaveSamplesAndSingleEndDNASeqData(project,
                                                  filenames,
                                                  extension,
                                                  seqRun,
                                                  aveReadLen, 
                                                  readPrefix=prefix)
    elif dataType == api.getDataTypes().DNA_SEQ_PAIRED_END:
        seqRun = UserChoice('sequencer_type', api.getExperiments(dataType=dataType),
                            new=lambda : addExperiment(dataType=dataType)).resolve()
        extension1 = UserInput('Please enter the file extension for the forward read files', '_1.fastq.gz').resolve()
        extension2 = UserInput('Please enter the file extension for the reverse read files', '_2.fastq.gz').resolve()
        prefix = UserInput('Optionally, indicate a prefix for the read files',default='').resolve()
        aveReadLen = UserInput('What is the average read length', 101, type=int).resolve()
        aveGapLen = UserInput('What is the average gap length, if known', None, type=int).resolve()
        api.bulkSaveSamplesAndPairedEndDNASeqData(project,
                                                  filenames,
                                                  extension1,
                                                  extension2,
                                                  seqRun,
                                                  aveReadLen,
                                                  aveGapLen=aveGapLen,
                                                  readPrefix=prefix)
@add.command(name='project')
@click.option('-n', '--name', default=None, help='The project name')
def cli_addProject(name=None):
    addProject(name=name)
    
def addProject(name=None):
    tryAgain = True
    while tryAgain:
        tryAgain=False
        if not name:
            name = UserInputNoDefault('What is the name of the project').resolve()
        if api.getProject(name):
            tryAgain= True
            sys.stderr.write('Project {} already exists. Please pick a new name.\n'.format(name))
            name=None
    api.saveProject(name,None)

@add.command(name='experiment')
@click.option('-n', '--name', default=None, help='The experiment name')
def cli_addExperiment(name=None, dataType=None):
    addExperiment(name=name, dataType=dataType)
    
def addExperiment(name=None, dataType=None):
    if not dataType:
            dataType = UserChoice('data_type', api.getDataTypes()).resolve()
    tryAgain = True
    while tryAgain:
        tryAgain=False
        if not name:
            name = UserInputNoDefault('What is the name of the experiment').resolve()
        if api.getExperiment(name):
            tryAgain= True
            sys.stderr.write('Experiment {} already exists. Please pick a new name.\n'.format(name))
            name=None
    api.saveExperiment(name, dataType, None)

@add.command(name='sample')
@click.option('-n', '--name', default=None, help='The sample name')
@click.option('-p', '--project', default=None, help='The project name')
def cli_addSample(name=None, project=None):
    addSample(name=name, project=project)
    
def addSample(name=None, project=None):
    if not project:
        project = UserChoice('project', api.getProjects(), new=addProject()).resolve()
    elif not api.getProject(project):
        add = BoolUserInput('Project {} not. found Would you like to add it?'.format(project),False)
        if not add:
            sys.stderr.write('No project {}. Exiting.\n'.format(project))
            sys.exit(1)
        else:
            addProject(name=project)
        project = api.getProject(project)

    tryAgain = True
    while tryAgain:
        tryAgain=False
        if not name:
            name = UserInputNoDefault('What is the name of the sample').resolve()
        if api.getSample(name):
            tryAgain= True
            sys.stderr.write('Sample {} already exists. Please pick a new name.\n'.format(name))
            name=None
    api.saveSample(name,project, None)
    

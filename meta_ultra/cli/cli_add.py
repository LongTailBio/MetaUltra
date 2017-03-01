from meta_ultra.user_input import *
import meta_ultra.api as api
from .cli import main
import click
import meta_ultra.conf_builder as conf_builder

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
    if dataType == api.getDataTypes().WGS_DNA_SEQ_SINGLE_END:
        seqRun = UserChoice('sequencer_type', api.getExperiments(dataTypes=[dataType]),
                            new=lambda : addExperiment(dataType=dataType)).resolve()
        nfiles = 0
        while nfiles == 0:
            extension = UserInput('Please enter the file extension for the read files', '.fastq.gz').resolve()
            for filename in filenames:
                if extension in filename:
                    nfiles += 1
            if nfiles == 0:
                sys.stderr.write('No files match extension.\n')
            else:
                sys.stderr.write('{} files match extension\n'.format(nfiles))
        prefix = UserInput('Optionally, indicate a prefix for the read files', '').resolve()
        aveReadLen = UserInputNoDefault('What is the average read length', type=int).resolve()
        samples, seqData = api.bulkSaveSamplesAndSingleEndDNASeqData(project,
                                                                     sampleType,
                                                  filenames,
                                                  extension,
                                                  seqRun,
                                                  aveReadLen, 
                                                  readPrefix=prefix)
    elif dataType == api.getDataTypes().WGS_DNA_SEQ_PAIRED_END:
        seqRun = UserChoice('sequencer_type', api.getExperiments(dataTypes=[dataType]),
                            new=lambda : addExperiment(dataType=dataType)).resolve()

        nfiles = 0
        while nfiles == 0:
            extension1 = UserInput('Please enter the file extension for the forward read files', '_1.fastq.gz').resolve()
            for filename in filenames:
                if extension1 in filename:
                    nfiles += 1
            if nfiles == 0:
                sys.stderr.write('No files match extension.\n')
            else:
                sys.stderr.write('{} files match extension\n'.format(nfiles))


        nfiles = 0
        while nfiles == 0:
            extension2 = UserInput('Please enter the file extension for the reverse read files', '_2.fastq.gz').resolve()
            for filename in filenames:
                if extension2 in filename:
                    nfiles += 1
            if nfiles == 0:
                sys.stderr.write('No files match extension.\n')
            else:
                sys.stderr.write('{} files match extension\n'.format(nfiles))

        prefix = UserInput('Optionally, indicate a prefix for the read files',default='').resolve()
        aveReadLen = UserInputNoDefault('What is the average read length', type=int).resolve()
        aveGapLen = UserInput('What is the average gap length, if known', None, type=int).resolve()
        samples, seqData = api.bulkSaveSamplesAndPairedEndDNASeqData(project,
                                                                     sampleType,
                                                  filenames,
                                                  extension1,
                                                  extension2,
                                                  seqRun,
                                                  aveReadLen,
                                                  aveGapLen=aveGapLen,
                                                  readPrefix=prefix)

    sys.stderr.write('Added {} data records.\n'.format(len(seqData)))
    for dataRec in seqData:
        sys.stderr.write('{}\n'.format(dataRec))
        
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
@click.option('--sample-type', default=None, help='The sample type')
@click.option('-p', '--project', default=None, help='The project name')
def cli_addSample(name=None, sample_type=None ,project=None):
    addSample(name=name, sampleType=sample_type, project=project)
    
def addSample(name=None, project=None, sampleType=None):
    if not project:
        project = UserChoice('project', api.getProjects(), new=addProject).resolve()
    if not sampleType:
        sampleType = UserChoice('sample_type', api.getSampleTypes()).resolve()
    sampleType = SampleType.asSampleType(sampleType)
    if not api.getProject(project):
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
    api.saveSample(name,sampleType,project, None)
    

@add.command(name='conf')
@click.option('-n', '--name', default=None, help='The sample name')
@click.option('--default/--no-default',default=False,help='accept defaults')
@click.option('--fine-control/--no-fine-control',default=False,help='control every aspect')
def cli_addConf(name, default, fine_control):
    return addConf(name=name, useDefaults=default, fineControl=fine_control)

def addConf(name=None, useDefaults=None, fineControl=None):
    if not name:
        name = UserInputNoDefault('What is the name of this conf?').resolve()
    if not fineControl and useDefaults is None:
        useDefaults = BoolUserInput('Accept all default parameters for this conf?', False).resolve()
    if fineControl is None and not useDefaults:
        fineControl = BoolUserInput('Control absolutely every aspect of this conf?', False).resolve()

    return conf_builder.buildNewConf(name, useDefaults=useDefaults, fineControl=fineControl)
    

from meta_ultra.user_input import *
import meta_ultra.api as api




def addData(filenames):
    project = UserChoice('project', api.getProjects(), new=addProject()).resolve()
    sampleType = UserChoice('sample_type', api.getSampleTypes()).resolve()
    dataType = UserChoice('data_type', api.getDataTypes()).resolve()
    if dataType == api.getDataTypes().DNA_SEQ_SINGLE_END:
        seqRun = UserChoice('sequencer_type', api.getExperiments(dataType=dataType), new=addExperiment(dataType=dataType)).resolve()
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
        seqRun = UserChoice('sequencer_type', api.getExperiments(dataType=dataType), new=addExperiment(dataType=dataType)).resolve()
        extension1 = UserInput('Please enter the file extension for the forward read files', '_1.fastq.gz').resolve()
        extension2 = UserInput('Please enter the file extension for the reverse read files', '_2.fastq.gz').resolve()
        prefix = UserInput('Optionally, indicate a prefix for the read files',default='').resolve()
        aveReadLen = UserInput('What is the average read length', 101, type=int).resolve()
        aveGapLen = UserInput('What is the average gap length, if known', None, type=int).resolve()
        api.bulkSaveSamplesAndPairedEndDNASeqData(project,
                                                  filenames,
                                                  extension1,
                                                  extension2
                                                  seqRun,
                                                  aveReadLen,
                                                  aveGapLen=aveGapLen,
                                                  readPrefix=prefix)
        
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

    
def addSample(name=None, projectName=None):
    if not projectName:
        project = UserChoice('project', api.getProjects(), new=addProject()).resolve()
    elif not api.getProject(name):
        add = BoolUserInput('Project {} not. found Would you like to add it?'.format(name),False)
        if not add:
            sys.stderr.write('No project {}. Exiting.\n'.format(name))
            sys.exit(1)
        else:
            addProject(name=name)
        project = api.getProject(name)

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
    

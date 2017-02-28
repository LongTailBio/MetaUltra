from .api_utils import *
import meta_ultra.config as config
from meta_ultra.data_type import DataType
from meta_ultra.sample_type import SampleType
from meta_ultra.database import *
import os.path
import os

################################################################################
#
# Add data to the working area
#
################################################################################

def saveSingleEndDNASeqData(name,
			    readFilename,
			    aveReadLen,
			    sample,
			    experiment,
			    project):
    if type(sample) != str:
        sample = sample.name
    if type(experiment) != str:
        experiment = experiment.name
    if type(project) != str:
        project = project.name
    dataRec = SingleEndDNASeqData(name=name,
				  reads_1=readFilename,
				  ave_read_length=aveReadLen,
				  sample_name=sample,
				  project_name=project,
				  experiment_name=experiment)
    return dataRec.save()
	
def savePairedEndDNASeqData(name,
			   read1Filename,
			   read2Filename,
			   aveReadLen,
			   sample,
			   experiment,
			   project,
			   aveGapLen=None):
    if type(sample) != str:
        sample = sample.name
    if type(experiment) != str:
        experiment = experiment.name
    if type(project) != str:
        project = project.name
    dataRec = PairedEndDNASeqData(name=name,
				 reads_1=read1Filename,
				 reads_2=read2Filename,
				 ave_read_length=aveReadLen,
				 sample_name=sample,
				 project_name=project,
				 experiment_name=experiment,
				 ave_gap_len=aveGapLen)
    return dataRec.save()



################################################################################
#
# Info Storage
#
################################################################################

def saveProject(name, metadata):
    proj = Project(**{'name': name, 'metadata': metadata})
    return proj.save()

###########################################################

def saveSample(name, sampleType, project, metadata):
    if type(project) != str:
        project = project.name
    sample = Sample(name=name,
                    sample_type=sampleType,
		    project_name=project,
		    metadata=metadata)
    return sample.save()

###########################################################

def saveExperiment(name, dataType, metadata):
    dataType = convertDataType(dataType)
    if dataType == DataType.WGS_DNA_SEQ_SINGLE_END:
        exp = SingleEndDNASeqRun(name=name, metadata=metadata)
    elif dataType == DataType.WGS_DNA_SEQ_PAIRED_END:
        exp = PairedEndDNASeqRun(name=name, metadata=metadata)
    else:
        raise DataTypeNotFoundError()
    
    return exp.save()

def saveSingleEndedSeqRun(name, metadata):
    return saveExperiment(name, SingleEndedSeqData.dataType(), metadata)

def savePairedEndedSeqRun(name, metadata):
    return saveExperiment(name, PairedEndedSeqData.dataType(), metadata)

###########################################################

def saveConf(name, confDict):
    conf = Conf(name=name, conf_dict=confDict)
    return conf.save()

###########################################################

def saveResult(name, resultFilenames, data, conf, sample, experiment, project):
    if type(sample) != str:
        sample = sample.name
    if type(conf) != str:
        conf = conf.name
    if type(project) != str:
        project = project.name
    if type(data) != str:
        data = data.name
    if type(experiment) != str:
        experiment = experiment.name
    result = Result(name=name,
		    data_name=data,
		    conf_name=conf,
		    sample_name=sample,
		    experiment_name=experiment,
		    project_name=project,
		    result_files=resultFilenames)
    return result.save()
		    

###########################################################
	
def bulkSaveSamplesAndSingleEndDNASeqData(project,
                                          sampleType,
					 filenames,
					 readSuffix,
					 singleEndedSeqRun,
					 aveReadLen,
					 modify=False,
					 readPrefix=None,
					 sampleNameFunc=lambda x: x,
					 metadataFunc=lambda x: None):
	samplesToFilenames = {}
	for filename in filenames:
		sample = basename(filename).split(readSuffix)[0]
		if readPrefix:
			sample = sample.split(readPrefix[-1])
		sample = sampleNameFunc(sample)
		samplesToFilenames[sample] = filename

	projectName = project
	if type(project) != str:
	    projectName = project.name
	ruName = singleEndedSeqRun
	if type(singleEndedSeqRun) != str:
	    runName = singleEndedSeqRun.name
	    
	seqDats = []
	samples = []
	for sampleName, filename in samplesToFilenames.items():
		sample = Sample(name=sampleName, sample_type=sampleType, project_name=projectName, metadata=metadataFunc(sampleName))
		if not sample.saved() or modify:
			sample.save(modify=modify)
		samples.append(sample)
		seqDataName='{}|{}|{}|seq1end'.format(projectName,sampleName,runName)
		seqData = SingleEndDNASeqData( name=seqDataName,
					  data_type='seq_single_ended',
					  sample_name=sampleName,
					  project_name=projectName,
					  reads_1=filename,
					  experiment_name=runName,
					  ave_read_length=aveReadLen)
		try:
		    seqData.save(modify=modify)
		    seqDats.append(seqData)
		except RecordExistsError:
		    pass
		
	return samples, seqDats

###########################################################

def bulkSaveSamplesAndPairedEndDNASeqData(project,
                                          sampleType,
					 filenames,
					 read1Suffix,
					 read2Suffix,
					 pairedEndSeqRun,
					 aveReadLen,
					 aveGapLen=None,
					 readPrefix=None,
					 sampleNameFunc=lambda x: x,
					  metadataFunc=lambda x: None,
                                          modify=False):
	samplesToFilenames = {}
	for filename in filenames:
		first=True
		if read1Suffix in filename:
			sample = basename(filename).split(read1Suffix)[0]
		elif read2Suffix in filename:
			first=False
			sample = basename(filename).split(read2Suffix)[0]
		else:
			continue
		if readPrefix:
			sample = sample.split(readPrefix[-1])
		sample = sampleNameFunc(sample)
		if sample not in samplesToFilenames:
			samplesToFilenames[sample] = {}
		if first:
			samplesToFilenames[sample]['1'] = filename
		else:
			samplesToFilenames[sample]['2'] = filename


	projectName = project
	if type(project) != str:
	    projectName = project.name
	ruName = pairedEndSeqRun
	if type(pairedEndSeqRun) != str:
	    runName = pairedEndSeqRun.name

			
	seqDats = []
	samples = []
	for sampleName, filenames in samplesToFilenames.items():
		reads1 = filenames['1']
		reads2 = filenames['2']
		sample = Sample(name=sampleName, sample_type=sampleType, project_name=projectName, metadata=metadataFunc(sampleName)) 
		if not sample.saved() or modify:
			sample.save(modify=modify)
		samples.append(sample)
		seqDataName='{}|{}|{}|seq2end'.format(projectName,sampleName, runName)
		seqData = PairedEndDNASeqData( name=seqDataName,
			   data_type='seq_paired_end',
			   sample_name=sampleName,
			   project_name=projectName,
			   reads_1=reads1,
			   reads_2=reads2,
			   experiment_name=runName,
			   ave_read_length=aveReadLen,
			   ave_gap_length=aveGapLen)
		try:
		    seqData.save(modify=modify)
		    seqDats.append(seqData)
		except RecordExistsError:
		    pass
		
	return samples, seqDats


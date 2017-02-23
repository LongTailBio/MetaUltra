from .api_utils import *
import meta_ultra.config as config
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
                                 ave_read_len=aveReadLen,
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
                                 ave_read_len=aveReadLen,
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
    proj = Project({'name': name, 'metadata': metadata})
    return proj.save()

###########################################################

def saveSample(name, project, metadata):
    if type(project) != str:
        project = project.name
    sample = Sample(name=name,
                    project_name=project,
                    metadata=metadata)
    return sample.save()

###########################################################

def saveExperiment(name, dataType, metadata):
    pass

def saveSingleEndedSeqRun(name, metadata):
    return saveExperiment(name, SingleEndedSeqData.dataType(), metadata)

def savePairedEndedSeqRun(name, metadata):
    return saveExperiment(name, PairedEndedSeqData.dataType(), metadata)

###########################################################

def saveConf(name, confDict):
    raise NotImplementedError()

###########################################################

def saveResult(name, resultFilenames, data, conf, sample, project):
    if type(sample) != str:
        sample = sample.name
    if type(conf) != str:
        conf = conf.name
    if type(project) != str:
        project = project.name
    if type(data) != str:
        data = data.name
    result = Result(name=name,
                    data_name=data,
                    conf_name=conf,
                    sample_name=sample,
                    project_name=project,
                    result_files=resultFilenames)
    return result.save()
                    

###########################################################
	
def bulkSaveSamplesAndSingleEndDNASeqData(project,
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

	seqDats = []
	samples = []
	for sampleName, filename in samplesToFilenames.items():
		sample = Sample(name=sampleName, project_name=projectName, metadata=metadataFunc(sampleName))
		if not sample.saved() or modify:
			sample.save(modify=modify)
		samples.append(sample)
		seqDataName='{}|{}|{}|seq1end'.format(projectName,sampleName,singleEndedSeqRun.machineType)
		seqData = SingleEndedSeqData( name=seqDataName,
					  data_type='seq_single_ended',
					  sample_name=sampleName,
					  project_name=projectName,
					  reads_1=filename,
					  experiment_name=singleEndedSeqRun.name,
					  ave_read_length=aveReadLen)
		seqData.save(modify=modify)
		seqDats.append(seqData)
	return samples, seqDats

###########################################################

def bulkSaveSamplesAndPairedEndedSeqData(project,
			                 filenames,
			                 read1Suffix,
			                 read2Suffix,
			                 pairedEndSeqRun,
			                 aveReadLen,
			                 aveGapLen=None,
			                 readPrefix=None,
			                 sampleNameFunc=lambda x: x,
			                 metadataFunc=lambda x: None):
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

	seqDats = []
	samples = []
	for sampleName, filenames in samplesToFilenames.items():
		reads1 = filenames['1']
		reads2 = filenames['2']
		sample = Sample(name=sampleName, project_name=projectName, metadata=metadataFunc(sampleName)) 
		if not sample.saved() or modify:
			sample.save(modify=modify)
		samples.append(sample)
		seqDataName='{}|{}|{}|seq2end'.format(projectName,sampleName,pairedEndSeqRun.machineType)
		seqData = PairedEndedSeqData( name=seqDataName,
			   data_type='seq_paired_end',
			   sample_name=sampleName,
			   project_name=projectName,
			   reads_1=reads1,
			   reads_2=reads2,
			   experiment_name=pairedEndSeqRun.name,
			   ave_read_length=aveReadLen,
			   ave_gap_length=aveGapLen)
	seqData.save(modify=modify)
	seqDats.append(seqData)
	return samples, seqDats


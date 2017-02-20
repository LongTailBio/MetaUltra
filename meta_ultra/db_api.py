
from meta_ultra.database import *

def toNameList(l):
    if not l:
        return []
    names = []
    for el in l:
        if type(el) == str:
            names.append(el)
        else:
            names.append(el.name)
    return names

################################################################################
#
# Info Retrieval
#
################################################################################

def getProjects():
    pass

############################################################

def getExperiments():
    pass

############################################################

def getConfs():
    pass

###########################################################

def getSamples(projects=None):
    projNames = toNameList(projects)

###########################################################
    
def getData(dataType=None, samples=None, experiments=None, projects=None):
    sampleNames = toNameList(samples)
    expNames = toNameList(experiments)
    projNames = toNameList(projects)

def getSingleEndedSeqData(samples=None, experiments=None, projects=None):
    return getData(SingleEndedSeqData.dataType(),
                   samples=samples,
                   experiments=experiments,
                   projects=projects
                   )

def getPairedEndedSeqData(samples=None, experiments=None, projects=None):
    return getData(PairedEndedSeqData.dataType(),
                   samples=samples,
                   experiments=experiments,
                   projects=projects
                   )


################################################################################
#
# Info Storage
#
################################################################################

def saveProject(name, metadata):
    pass

###########################################################

def saveSample(name, project, metadata):
    pass

###########################################################

def saveExperiment(name, dataType, metadata):
    pass

def saveSingleEndedSeqRun(name, metadata):
    return saveExperiment(name, SingleEndedSeqData.dataType(), metadata)

def savePairedEndedSeqRun(name, metadata):
    return saveExperiment(name, PairedEndedSeqData.dataType(), metadata)

###########################################################

def saveSingleEndedSeqData(name,
                           readFilename,
                           aveReadLen,
                           sample,
                           experiment,
                           project):
    pass

def savePairedEndedSeqData(name,
                           read1Filename,
                           read2Filename,
                           aveReadLen,
                           sample,
                           experiment,
                           project,
                           aveGapLen=None):
    pass

###########################################################

def saveResult(name, resultFilenames, data, conf, sample, project):
    pass

###########################################################
	
def bulkSaveSamplesAndSingleEndedSeqData(projectName,
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


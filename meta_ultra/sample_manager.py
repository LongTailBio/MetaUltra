
from meta_ultra.database import *


################################################################################
#
# Factory Functions
#
################################################################################
    
def add_single_ended_seq_data(projectName,
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

################################################################################

def add_paired_ended_seq_data(projectName,
                        filenames,
                        read1Suffix,
                        read2Suffix,
                        pairedEndSeqRun,
                        aveReadLen,
                        aveGapLen=None,
                        modify=False,
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

################################################################################
#
# Retrieval Functions
#
################################################################################

def getSamples(projectName=None):
    if projectName:
        return Sample.search(where('project_name') == projectName)
    return Sample.all()

def getData(sample):
    datas = Data.search(where('sample_name') == sample.name)
    return datas

def get_samples_with_seq_data():
    sampleList = {}
    for sampleJSON in sampleTbl.all():
        sample = Sample(**sampleJSON)
        seqDataRecs = dataTbl.search((where('sample_name') == sample.name) &
                                        (where('project_name') == sample.projectName))

        sampleList[sample] = seqDataRecs
    return sampleList

from tinydb import TinyDB, Query, where
import meta_ultra.config as config
from meta_ultra.utils import *
from os.path import basename

db = TinyDB(config.db_file)
sampleTbl = db.table(config.db_sample_table)
dataTbl = db.table(config.db_data_table)
experimentTbl = db.table(config.db_experiment_table)

def getOrNone(key,dict):
    try:
        return dict[key]
    except KeyError:
        return None

################################################################################
#
# Classes
#
################################################################################

class RecordExistsError(Exception):
    pass

class DataTypeNotFoundError(Exception):
    pass

def checkDataType(dataType):
    types = ['seq_single_ended',
             'seq_paired_ended']
    if dataType in types:
        return dataType
    raise DataTypeNotFoundError() 

class Record:
    def __init__(self, name, dbTbl):
        self.name = name
        self.dbTbl = dbTbl
        self.fileNames = []

    def registerFile(self, fname):
        self.fileNames.append(fname)

    def exists(self):
        return self.dbTbl.get(where('name') == self.name) != None

    def record(self):
        return self.dbTbl.get(where('name') == self.name)
    
    def save(self,modify=False):
        if self.exists() and not modify:
            raise RecordExistsError()
        elif modify:
            rec = self.record()
            return self.dbTbl.update(self.to_dict(), eids=[rec.eid])
        else:
            return self.dbTbl.insert(self.to_dict())

################################################################################

class Data( Record):
    def __init__(self, name, dataType, sampleName, projectName, experimentName):
        super(Data, self).__init__(name, dataTbl)
        self.dataType = checkDataType(dataType)
        self.sampleName = sampleName
        self.projectName = projectName
        self.experimentName = experimentName
        
    def to_dict(self):
        out = {
            'name': self.name,
            'data_type': self.dataType,
            'sample_name':self.sampleName,
            'project_name': self.projectName,
            'experiment_name':self.experimentName
            }
        self._to_dict(out)
        return out

    
class SingleEndedSeqData(Data):

    def __init__(self,**kwargs):
        super(SingleEndedSeqData, self).__init__(kwargs['name'],
                                                 'seq_single_ended',
                                                 kwargs['sample_name'],
                                                 kwargs['project_name'],
                                                 kwargs['experiment_name'])
        self.reads1 = kwargs['reads_1']
        self.registerFile(self.reads1)
        self.aveReadLen = int(kwargs['ave_read_length'])

    def _to_dict(self, out):
        out['reads_1'] = self.reads1,
        out['ave_read_length'] = self.aveReadLen
        return out


class PairedEndedSeqData(Data):

    def __init__(self,**kwargs):
        super(PairedEndedSeqData, self).__init__(kwargs['name'],
                                                 'seq_paired_ended',
                                                 kwargs['sample_name'],
                                                 kwargs['project_name'],
                                                 kwargs['experiment_name'])
        self.reads1 = kwargs['reads_1']
        self.registerFile(self.reads1)
        self.reads2 = kwargs['reads_2']
        self.registerFile(self.reads2)
        self.aveReadLen = int(kwargs['ave_read_length'])
        self.aveGapLen = int(kwargs['ave_gap_length'])

    def _to_dict(self, out):
        out['reads_1'] = self.reads1,
        out['reads_2'] = self.reads2,
        out['ave_read_length'] = self.aveReadLen
        out['ave_gap_length'] = self.aveGapLen
        return out

################################################################################

class Experiment(Record):
    def __init__(self, name, dataType):
        super(Experiment, self).__init__(name,experimentTbl)
        self.dataType = checkDataType(dataType)

    def to_dict(self):
        out = {
            'name': self.name,
            'data_type': self.dataType
        }
        self._to_dict(out)
        return(out)
    
class SingleEndedSequencingRun( Experiment):
    def __init__(self,**kwargs):
        super(SingleEndedSequencingRun, self).__init__(kwargs['name'],
                                                       'seq_single_ended')
        self.machineType = kwargs['machine_type']

    def _to_dict(self,out):
        out['machine_type'] = self.machineType
        return out

class PairedEndedSequencingRun( Experiment):
    def __init__(self,**kwargs):
        super(PairedEndedSequencingRun, self).__init__(kwargs['name'],
                                                       'seq_paired_ended')
        self.machineType = kwargs['machine_type']

    def _to_dict(self,out):
        out['machine_type'] = self.machineType
        return out

    
################################################################################
        
class Sample(Record):
    def __init__(self,**kwargs):
        super(Sample, self).__init__(kwargs['name'],
                                     sampleTbl)
        self.projectName = kwargs['project_name']
        if 'metadata' in kwargs:
            self.metadata = kwargs['metadata']
        else:
            self.metadata = {}

    def to_dict(self):
        out = {
            'name' : self.name,
            'project_name':self.projectName,
            'metadata':self.metadata
            }
        return out

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
        if not sample.exists() or modify:
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
        if not sample.exists() or modify:
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


def get_samples_with_seq_data():
    sampleList = {}
    for sampleJSON in sampleTbl.all():
        sample = Sample(**sampleJSON)
        seqDataRecs = dataTbl.search((where('sample_name') == sample.name) &
                                        (where('project_name') == sample.projectName))

        sampleList[sample] = seqDataRecs
    return sampleList

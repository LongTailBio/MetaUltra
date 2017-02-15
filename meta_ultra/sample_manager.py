from tinydb import TinyDB, Query, where
import meta_ultra.config as config
from meta_ultra.utils import *
from os.path import basename

db = TinyDB(config.db_file)
sampleTbl = db.table(config.db_sample_table)
seqDataTbl = db.table(config.db_seq_data_table)
seqRunTbl = db.table(config.db_seq_run_table)

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

class SeqData:

    def __init__(self,**kwargs):
        self._name = kwargs['name']
        self.sampleId = kwargs['sample_id']
        self.projectName = kwargs['project_name']
        self.paired = kwargs['paired']
        self.reads_1 = kwargs['reads_1']
        if self.paired:
            self.reads_2 = kwargs['reads_2']
            self.aveGapLen = int(getOrNone('ave_gap_length', kwargs))
        self.sequencingRun = getOrNone('sequencing_run', kwargs)
        self.aveReadLen = int(kwargs['ave_read_length'])

    def to_dict(self):
        out = {
            'name': self.name(),
            'sample_id': self.sampleId,
            'project_name': self.projectName,
            'paired': self.paired,
            'reads_1': self.reads_1,
            'sequencing_run': self.sequencingRun.to_dict(),
            'ave_read_length': self.aveReadLen
            }
        if self.paired:
            out['reads_2'] = self.reads_2
            out['ave_gap_length'] = self.aveGapLen
        return out

    def exists(self):
        return seqDataTbl.get(where('name') == self.name())

    def eid(self):
        if not self.exists():
            return None
        rec = self._dbget()
        return rec.eid

    def name(self):
        return self._name

    def _dbget(self):
        rec = seqDataTbl.get(where('name') == self.name())
        return rec
    
    def save(self,modify=False):
        rec = self._dbget()
        if rec and not modify:
            raise RecordExistsError()
        elif modify:
            return seqDataTbl.update(self.to_dict(), eids=[rec.eid])
        else:
            return seqDataTbl.insert(self.to_dict())

################################################################################
    
class SequencingRun:
    def __init__(self,**kwargs):
        self._machineType = kwargs['machine_type']

    def machineType(self):
        return self._machineType

    def to_dict(self):
        out = {
            'machine_type':self.machineType()
            }
        return out

    def exists(self):
        return seqRunTbl.contains(where('machine_type') == self.machineType())

    def _dbget(self):
        rec = seqRunTbl.get(where('machine_type') == self.machineType())
        return rec
    
    def eid(self):
        if not self.exists():
            return None
        rec = self._dbget()
        return rec.eid
    
    def save(self, modify=False):
        rec = self._dbget()
        if rec and not modify:
            raise RecordExistsError()
        elif modify:
            return seqRunTbl.update(self.to_dict(), eids=[rec.eid])
        else:
            return seqRunTbl.insert(self.to_dict())

################################################################################
        
class Sample:
    def __init__(self,**kwargs):
        self._sampleId = kwargs['sample_id']
        self.projectName = kwargs['project_name']
        self.metadata = getOrNone('metadata',kwargs)

    def sampleId(self):
        return self._sampleId

    def to_dict(self):
        out = {
            'sample_id': self.sampleId(),
            'project_name':self.projectName,
            }
        if self.metadata:
            out['metadata'] = self.metadata
        return out

    def _dbget(self):
        rec = sampleTbl.get((where('sample_id') == self.sampleId) &
                            (where('project_name') == self.projectName))
        return rec
    
    def save(self,modify=False):
        rec = self._dbget()
        if rec and not modify:
            raise RecordExistsError()
        elif modify:
            return sampleTbl.update(self.to_dict(), eids=[rec.eid])
        else:
            return sampleTbl.insert(self.to_dict())
        
    def exists(self):
        return sampleTbl.contains((where('sample_id') == self.sampleId) &
                                  (where('project_name') == self.projectName))

    def eid(self):
        if not self.exists():
            return None
        rec = self._dbget()
        return rec.eid

################################################################################
#
# Factory Functions
#
################################################################################
    
def add_single_ended_seq_data(projectName,
                        filenames,
                        readSuffix,
                        sequencingRun,
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

    for sampleName, filename in samplesToFilenames.items():
        sample = Sample(sample_id=sampleName, project_name=projectName, metadata=metadataFunc(sampleName))
        if not sample.exists():
            sample.save()
        seqDataName='{}|{}|{}'.format(projectName,sampleName,sequencingRun.machineType())
        seqData = SeqData( name=seqDataName,
                           sample_id=sampleName,
                           project_name=projectName,
                           paired=False,
                           reads_1=filename,
                           sequencing_run=sequencingRun,
                           ave_read_length=aveReadLen)
        seqData.save(modify=modify)

################################################################################

def add_paired_ended_seq_data(projectName,
                        filenames,
                        read1Suffix,
                        read2Suffix,
                        sequencingRun,
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

    for sampleName, filenames in samplesToFilenames.items():
        reads1 = filenames['1']
        reads2 = filenames['2']
        sample = Sample(sample_id=sampleName, project_name=projectName, metadata=metadataFunc(sampleName))
        if not sample.exists():
            sample.save()
        seqDataName='{}|{}|{}'.format(projectName,sampleName,sequencingRun.machineType())
        seqData = SeqData( name=seqDataName,
                           sample_id=sampleName,
                           project_name=projectName,
                           paired=False,
                           reads_1=reads1,
                           reads_2=reads2,
                           sequencer=sequencer,
                           ave_read_length=aveReadLen,
                           ave_gap_length=aveGapLen)
        seqData.save(modify=modify)

################################################################################
#
# Retrieval Functions
#
################################################################################


def get_samples_with_seq_data():
    sampleList = {}
    for sampleJSON in sampleTbl.all():
        sample = Sample(**sampleJSON)
        seqDataRecs = seqDataTbl.search((where('sample_id') == sample.sampleId()) &
                                        (where('project_name') == sample.projectName))

        sampleList[sample] = seqDataRecs
    return sampleList

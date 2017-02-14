from tinydb import TinyDB, Query
import meta_ultra.config as config
from meta_utlra.utils import *
from os.path import basename

db = TinyDB(config.db_file)
sampleTbl = dbtable(config.db_sample_table)
seqDataTbl = dbtable(config.db_seq_data_table)
seqRunTbl = dbtable(config.db_seq_run_table)

def getOrNone(key,dict):
    try:
        return dict[key]
    except KeyError:
        return None
    
class SeqData:

    def __init__(self,**kwargs):
        self.name = kwargs['name']
        self.sampleId = kwargs['sample_id']
        self.projectName = kwargs['project_name']
        self.paired = kwargs['paired']
        self.reads_1 = kwargs['reads_1']
        if self.paired:
            self.reads_2 = kwargs['reads_2']
            self.aveGapLen = int(getOrNone('ave_gap_length', kwargs))
        self.sequencingRun = getOrNone('sequencing_run', kwargs)
        self.aveReadLen = int(getOrNone('ave_read_length', kwargs))

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

    def name(self):
        return self.name

    def save(self,modify=False):
        rec = seqDataTbl.get(where('sample_id') == self.sampleId and where('name') == self.projectName)
        if rec and not modify:
            raise RecordExistsError()
        elif modify:
            seqDataTbl.update(self.to_dict(), eids=[rec.eid])
        else:
            seqDataTbl.insert(self.to_dict())
    
    
class SequencingRun:
    def __init__(self,type):
        self.type = type

    def type(self):
        return self.type

    def to_dict(self):
        out = {
            'machine_type':self.type()
            }
        return out

    def save(self, modify=False):
        rec = seqRunTbl.get(where('machine_type') == self.sampleId)
        if rec and not modify:
            raise RecordExistsError()
        elif modify:
            seqRunTbl.update(self.to_dict(), eids=[rec.eid])
        else:
            seqRunTbl.insert(self.to_dict())

class Sample:
    def __init__(self,sampleId, projectName, metadata=None):
        self.sampleId = sampleId
        self.projectName = projectName
        self.metadata = metadata

    def sampleId(self):
        return self.sampleId

    def to_dict(self):
        out = {
            'sample_id': self.sampleId(),
            'project_name':self.projectName,
            }
        if self.metadata:
            out['metadata'] = self.metadata
        return out

    def save(self,modify=False):
        rec = sampleTbl.get(where('sample_id') == self.sampleId and where('project_name') == self.projectName)
        if len(rec) > 0 and not modify:
            raise RecordExistsError()
        elif modify:
            sampleTbl.update(self.to_dict(), eids=[rec.eid])
        else:
            sampleTbl.insert(self.to_dict())
        
    def exists(self):
        return sampleTbl.contains(where('sample_id') == self.sampleId and where('project_name') == self.projectName)


    def __init__(self,**kwargs):
        self.name = kwargs['name']
        self.sampleId = kwargs['sample_id']
        self.projectName = kwargs['project_name']
        self.paired = kwargs['paired']
        self.reads_1 = kwargs['reads_1']
        if self.paired:
            self.reads_2 = kwargs['reads_2']
            self.aveGapLen = int(getOrNone('ave_gap_length', kwargs))
        self.sequencer = getOrNone('sequencer', kwargs)
        self.aveReadLen = int(getOrNone('ave_read_length', kwargs))

    
def add_single_ended_seq_data(projectName,
                        filenames,
                        readSuffix,
                        sequencingRun,
                        aveReadLen,
                        modify=True,
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
        sample = Sample(sampleName, projectName, metadataFunc(sampleName))
        if not sample.exists():
            sample.save()
        seqDataName='{}|{}|{}'.format(projectName,sampleName,sequencingRun.type())
        seqData = SeqData( name=seqDataName,
                           sample_id=sampleName,
                           project_name=projectName,
                           paired=False,
                           reads_1=filename,
                           sequencer=sequencer,
                           ave_read_len=aveReadLen)
        seqData.save(modify=modify)


def add_paired_ended_seq_data(projectName,
                        filenames,
                        read1Suffix,
                        read2Suffix,
                        sequencingRun,
                        aveReadLen,
                        aveGapLen=None,
                        modify=True,
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
        sample = Sample(sampleName, projectName, metadataFunc(sampleName))
        if not sample.exists():
            sample.save()
        seqDataName='{}|{}|{}'.format(projectName,sampleName,sequencingRun.type())
        seqData = SeqData( name=seqDataName,
                           sample_id=sampleName,
                           project_name=projectName,
                           paired=False,
                           reads_1=reads1,
                           reads_2=reads2,
                           sequencer=sequencer,
                           ave_read_len=aveReadLen,
                           ave_gap_len=aveGapLen)
        seqData.save(modify=modify)

from .api_utils import *
import meta_ultra.config as config
from meta_ultra.data_type import DataType
from meta_ultra.sample_type import SampleType
from meta_ultra.database import *
from .getters import *
import os.path
import os

################################################################################
#
# Add records to the repo
#
################################################################################


def newSampleGroup(name, samples=[], metadata={}, repo=None):
    pass

def renameSampleGroup(name, newName, repo=None):
    pass

def addMetadataToSampleGroup(name, metadata, repo=None):
    pass

def newSample(name, sampleType, metadata, repo=None):
    pass

def renameSample(name, newName, repo=None):
    pass

def addMetadataToSample(name, metadata, repo=None):
    pass


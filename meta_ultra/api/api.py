import meta_ultra.config as config
from meta_ultra.database import *
import os.path
import os
from snakemake import snakemake
from .api_utils import *

################################################################################
#
# Start a working area
#
################################################################################

def init(dir='.'):
    muDir = os.path.join(dir, config.mu_dir)
    os.mkdirs(muDir)

################################################################################
#
# Run modules
#
################################################################################

def runModules(conf,dataRecs,dryrun=False,unlock=False,rerun=False):
    confName = toName(conf)
    confWithData = ConfBuilder.addSamplesToConf(confName, dataRecs)
    return snakemake(config.snake_file,
                     config=confWithData,
                     cluster=config.cluster_wrapper,
                     keepgoing=True,
                     printshellcmds=True,
                     dryrun=dryrun,
                     unlock=unlock,
                     force_incomplete=rerun,
                     cores=njobs)
    

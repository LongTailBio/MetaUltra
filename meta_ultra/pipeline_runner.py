
import subprocess as sp
import meta_ultra.config as config
import sys
import meta_ultra.conf_builder as ConfBuilder
from json import dumps as jdumps
from tempfile import NamedTemporaryFile
from snakemake import snakemake

def run(confName,
        pairs=False,
        minReadLen=0,
        maxReadLen=250,
        njobs=1,
        dry_run=False,
        unlock=False,
        rerun=False):

    conf = ConfBuilder.add_samples_to_conf(confName,
                                           pairs=pairs,
                                           minReadLen=minReadLen,
                                           maxReadLen=maxReadLen)

    snakemake(config.snake_file,
              config=conf,
              cluster=config.cluster_wrapper,
              keepgoing=True,
              printshellcmds=True,
              dryrun=dry_run,
              unlock=unlock,
              force_incomplete=rerun,
              cores=njobs)


'''              
def result_info(conf, unlock=False):
    
    cmd = 'snakemake --snakefile {snkf} --configfile {conf} --detailed-summary'
    cmd = cmd.format(snkf=config.snake_file,
                     conf=conf,
                     )

    if unlock:
        cmd += ' --unlock'

    sys.stderr.write('Running: {}\n'.format(cmd))        
    sp.call(cmd,shell=True)
'''

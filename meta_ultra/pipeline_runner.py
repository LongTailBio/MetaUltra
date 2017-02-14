
import subprocess as sp
import meta_ultra.config as config
import sys
import meta_ultra.conf_builder as ConfBuilder
from json import dumps as jdumps
from tempfile import NamedTemporaryFile

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
    confFile = NamedTemporaryFile()
    confFile.write(jdumps(conf))
    cmd = 'snakemake --snakefile {snkf} --jobs {njobs} --configfile {conf} --cluster {cluster_wrapper} -k --printshellcmds'
    cmd = cmd.format(snkf=config.snake_file,
                     njobs=njobs,
                     conf=confFile.name,
                     cluster_wrapper=config.cluster_wrapper
                     )
    if dry_run:
        cmd += ' --dryrun'

    if unlock:
        cmd += ' --unlock'

    if rerun:
        cmd += ' --rerun-incomplete'
    
    sys.stderr.write('Running: {}\n'.format(cmd))        
    sp.call(cmd,shell=True)


def result_info(conf, unlock=False):
    
    cmd = 'snakemake --snakefile {snkf} --configfile {conf} --detailed-summary'
    cmd = cmd.format(snkf=config.snake_file,
                     conf=conf,
                     )

    if unlock:
        cmd += ' --unlock'

    sys.stderr.write('Running: {}\n'.format(cmd))        
    sp.call(cmd,shell=True)


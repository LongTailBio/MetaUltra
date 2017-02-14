
import subprocess as sp
import meta_ultra.config as config
import sys

def run(conf,njobs=1,dry_run=False,unlock=False,rerun=False):
    
    cmd = 'snakemake --snakefile {snkf} --jobs {njobs} --configfile {conf} --cluster {cluster_wrapper} -k --printshellcmds'
    cmd = cmd.format(snkf=config.snake_file,
                     njobs=njobs,
                     conf=conf,
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


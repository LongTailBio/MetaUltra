
import subprocess as sp
import meta_ultra.config as config
import sys

def run(conf,njobs=1,dry_run=False,unlock=False):
    
    cmd = 'snakemake --snakefile {snkf} --jobs {njobs} --configfile {conf} --cluster {cluster_wrapper} -k '
    cmd = cmd.format(snkf=config.snake_file,
                     njobs=njobs,
                     conf=conf,
                     cluster_wrapper=config.cluster_wrapper
                     )
    if dry_run:
        cmd += ' --dryrun'

    if unlock:
        cmd += ' --unlock'
    sys.stderr.write('Running: {}\n'.format(cmd))        
    sp.call(cmd,shell=True)
    

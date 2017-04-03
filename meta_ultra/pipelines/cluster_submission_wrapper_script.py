#!/usr/bin/env python3

import os
import sys
import subprocess as sp
from snakemake.utils import read_job_properties

jobscript = sys.argv[1]
job_properties = read_job_properties(jobscript)
#sys.stderr.write( open(jobscript).read())

cmd = 	(
	'ssh dcd3001@panda2.pbtech '
    	'qsub '  
	'-j y ' 
        '-cwd '  	
	'-N {job_name} '  
	'-l h_rt={wall_time_rqst} '   
	'-pe smp {n_cores} ' 
	'-l vf={n_gb_ram}G ' 
	'-l h_vmem={max_n_gb_ram}G ' 
	'-l os=rhel6.3 '
        '-l zenodotus=true '
    	'-V '
	'{cmd}')
        
cmd = 	cmd.format(job_name=job_properties['params']['job_name'],
                   wall_time_rqst='{}:00:00'.format(job_properties['resources']['time']),
                   n_cores=job_properties['threads'],
                   n_gb_ram=job_properties['resources']['n_gb_ram'],
                   max_n_gb_ram=2 * job_properties['resources']['n_gb_ram'],
                   cmd=jobscript
                   )
	
sys.stderr.write('\tRunning: "{}"\n'.format(cmd))
sp.call(cmd, shell=True)

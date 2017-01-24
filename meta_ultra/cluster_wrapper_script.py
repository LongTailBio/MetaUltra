#!/usr/bin/env python3

import os
import sys
import subprocess as sp
from snakemake.utils import read_job_properties

jobscript = sys.argv[1]
job_properties = read_job_properties(jobscript)


cmd = 	('qsub '  
	'-j y ' 
        '-cwd '  	
	'-N {job_name} '  
	'-l h_rt={wall_time_rqst} '   
	'-pe smp {n_cores} ' 
	'-l vf={n_gb_ram}G ' 
	'-l h_vmem={max_n_gb_ram}G ' 
	'-l os=rhel6.3 ' 
	'{cmd}')
        
cmd = 	cmd.format(job_name=job_properties['params']['job_name'],
                   wall_time_rqst='{}:00:00'.format(job_properties['resources']['time']),
                   n_cores=job_properties['threads'],
                   n_gb_ram=job_properties['resources']['n_gb_ram'],
                   max_n_gb_ram=2 * job_properties['resources']['n_gb_ram'],
                   cmd=jobscript
                   )
	
sys.stderr.write(cmd + '\n')
with open('foo','w') as f:
	f.write( open(jobscript).read())
sys.exit(1)

#sp.call('touch {}'.format(job_properties['output'][0]), shell=True)

# -*- coding: utf-8 -*-

import click
import meta_ultra.refs as refs
from meta_ultra.utils import *
import meta_ultra.conf_builder as conf_builder
import meta_ultra.pipeline_runner as pipeline_runner
import os.path
import json
from time import clock

@click.group()
def main():
    pass

@main.command()
@click.option('--tool', prompt='TOOL', help='The tool that the reference is intended to be used with')
@click.option('--name', prompt='NAME',default=None, help='Reference Name')
@click.option('--ref', prompt='FILE PATH', help='Location of reference')
def add_reference(tool,name,ref):
    refs.add_reference(tool,name,ref)

@main.command()
def list_references():
    refs.list_references()

@main.command()
@click.option('--single/--pairs', default=False, help='Reads are not pairwise')
@click.option('--defaults/--no-defaults',default=False,help='Use defaults')
@click.argument('samples', nargs=-1)
def new_conf(single, defaults, samples):
    pairs = not single
    myconf = conf_builder.build_conf(samples, pairs=pairs, use_defaults=defaults)
    print( json.dumps(myconf, sort_keys=True, indent=4))

@main.command()
@click.option('--dryrun/--normal',default=False,help='Print schedule but dont run anything')
@click.option('--unlock/--no-unlock',default=False,help='Unlock the working directory')
@click.option('--jobs',default=1,help='Number of jobs to run')
@click.option('--conf',prompt='CONF FILE', help='Conf file, can be generated using \'pmp conf\'')
def run( dryrun, unlock, jobs, conf):
	if not os.path.isfile(conf):
		sys.stderr.write('No conf file found. Exiting.\n')
		sys.exit(1)
        
	pipeline_runner.run(conf,dry_run=dryrun,njobs=jobs,unlock=unlock)

if __name__ == "__main__":
    main()

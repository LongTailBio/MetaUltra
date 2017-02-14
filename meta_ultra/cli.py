# -*- coding: utf-8 -*-

import click
import meta_ultra.refs as refs
import meta_ultra.tools  as tools
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
@click.option('-e','--eid', prompt='EID', type=int, default=None, help='Eid of reference record')
def remove_reference(eid):
    tools.remove_reference(eid)

    
@main.command()
@click.option('-n','--name', prompt='NAME',default=None, help='Tool name')
@click.option('-v','--version', prompt='VERSION', help='Version of tool')
@click.option('-e','--exc', prompt='EXC PATH', help='Path to executable')
def add_tool(name, version, exc):
    tools.add_tool(name, version,exc)

@main.command()
def list_tools():
    tools.list_tools()

@main.command()
@click.option('-e','--eid', prompt='EID',default=None, type=int, help='Eid of tool record')
def remove_tool(eid):
    tools.remove_tool(eid)

    
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
@click.option('--rerun-incomplete/--no-rerun-incomplete',default=False,help='Unlock the working directory')
def run( dryrun, unlock, jobs, conf, rerun_incomplete):
	if not os.path.isfile(conf):
		sys.stderr.write('No conf file found. Exiting.\n')
		sys.exit(1)
        
	pipeline_runner.run(conf,dry_run=dryrun,njobs=jobs,unlock=unlock,rerun=rerun_incomplete)

@main.command()
@click.option('--conf',prompt='CONF FILE', help='Conf file, can be generated using \'pmp conf\'')
@click.option('--unlock/--no-unlock',default=False,help='Unlock the working directory')
def result_info( conf, unlock):
	if not os.path.isfile(conf):
		sys.stderr.write('No conf file found. Exiting.\n')
		sys.exit(1)
        
	pipeline_runner.result_info(conf, unlock=unlock)

        
if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

import click
import meta_ultra.ref_manager as refs
import meta_ultra.tool_manager  as tools
from meta_ultra.utils import *
import meta_ultra.conf_builder as conf_builder
import meta_ultra.pipeline_runner as pipeline_runner
import meta_ultra.result_manager as result_manager
import os.path
import json
from time import clock

@click.group()
def main():
    pass

####################################################################################################

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

####################################################################################################
    
@main.command()
@click.option('--name', help='Conf Name')
@click.option('--defaults/--no-defaults',default=False,help='Use defaults')
def new_conf(name, defaults):
    pairs = not single
    myconf = conf_builder.build_and_save_new_conf(name, use_defaults=defaults)
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

####################################################################################################

@main.command()
@click.option('--project',default=None, help='Show only results from the given project')
@click.option('--sample',default=None, help='Show only results from the given sample')
def results(project,sample):
    results = result_manager.getResults(projectName=project,sampleName=sample)
    for result in results:
        print(result)

@main.command()
@click.option('--project',default=None, help='Show only samples from the given project')
@click.option('--data/--no-data',default=False, help='Show associated data for the samples')
def samples(project,data):
    samples = sample_manager.getSamples(projectName=project)
    for sample in samples:
        print(sample)
        if data:
            dataRecs = getData(sample)
            for dataRec in dataRecs:
                print('\t' + str(dataRec))



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

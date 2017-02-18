
# -*- coding: utf-8 -*-

import click
import meta_ultra.ref_manager as refs
import meta_ultra.tool_manager  as tools
from meta_ultra.utils import *
import meta_ultra.conf_builder as conf_builder
import meta_ultra.pipeline_runner as pipeline_runner
import meta_ultra.result_manager as result_manager
import meta_ultra.sample_manager as sample_manager
import meta_ultra.database as mupdb
import meta_ultra.modules as modules
import os.path
import json
from time import clock

@click.group()
def main():
    pass

####################################################################################################

@main.command()
@click.option('--default/--no-default', default=False, help='Use default toolsets.')
def list_modules(default):
    for module in modules.allModules(default=default):
        print(module)

@main.command()
@click.option('-i','--index', prompt='INDEX', type=int, help='Index of exec in toolset')
@click.option('-n','--name', prompt='NAME', help='Name of toolset')
@click.option('--confirm/--no-confirm', default=True, help='Do or do not confirm removal')
def remove_tool_from_module(index,name,confirm):
    module = modules.getModule(name)
    module.removeTool(index,confirm=confirm)

@main.command()
@click.option('--module-name', prompt='MODULE NAME', help='Name of module')
@click.option('--tool-name', prompt='TOOL NAME', help='Name of tool')
@click.option('--version', prompt='VERSION', help='Version of tool')
@click.option('--filepath', prompt='FILEPATH', help='Path to tool')
@click.option('--default/--no-default', default=False, help='Use default toolsets.')
def add_tool_to_module(module_name, tool_name, version, filepath, default):
    module = modules.getModule(module_name, default=default)
    print(module.buildAddTool(tool_name, version, filepath))

@main.command()
@click.option('-i','--index', prompt='INDEX', type=int, help='Index of reference in toolset')
@click.option('-n','--name', prompt='NAME', help='Name of module')
@click.option('--confirm/--no-confirm', default=True, help='Do or do not confirm removal')
def remove_ref_from_module(index,name,confirm):
    module = modules.getModule(name)
    module.removeRef(index,confirm=confirm)

@main.command()
@click.option('--module-name', prompt='MODULE NAME', help='Name of module')
@click.option('--ref-name', prompt='REF NAME', help='Name of reference')
@click.option('--tool-name', prompt='TOOl NAME', help='Name of tool')
@click.option('--filepath', prompt='FILEPATH', help='Path to reference')
@click.option('--default/--no-default', default=False, help='Use default toolsets.')
def add_ref_to_module(module_name, ref_name, tool_name, filepath, default):
    module = modules.getModule(module_name, default=default)
    print(module.buildAddRef(ref_name, tool_name, filepath))

@main.command()
@click.option('-n','--name', prompt='NAME', help='Name of toolset')
@click.option('--param-name', prompt='PARAM NAME', help='Name of parameter')
@click.option('--confirm/--no-confirm', default=True, help='Do or do not confirm removal')
def remove_param_from_module(name,param,confirm):
    module = modules.getModule(name)
    module.removeRef(index,confirm=confirm)

@main.command()
@click.option('--module-name', prompt='MODULE NAME', help='Name of module')
@click.option('--param-name', prompt='PARAM NAME', help='Name of parameter')
@click.option('--param-val', prompt='PARAM VAL', help='Value of parameter')
def add_param_to_module(module_name, param_name, param_val):
    module = modules.getModule(module_name)
    print(module.removeParam(param_name))

    
####################################################################################################
    
@main.command()
@click.option('--name', prompt='NAME', help='Conf Name')
@click.option('--defaults/--no-defaults',default=False,help='Use defaults')
@click.option('--fine-control/--no-fine-control',default=False,help='Enter values for every parameter')
@click.option('--modify/--no-modify',default=False,help='Modify an existing conf')
def new_conf(name, defaults, fine_control, modify):
    myconf = conf_builder.build_and_save_new_conf(name, useDefaults=defaults, fineControl=fine_control, modify=modify)
    print(myconf)

@main.command()
@click.option('--dryrun/--normal',default=False,help='Print schedule but dont run anything')
@click.option('--unlock/--no-unlock',default=False,help='Unlock the working directory')
@click.option('--jobs',default=1,help='Number of jobs to run')
@click.option('--conf',prompt='CONF NAME', help='Conf file, can be generated using \'pmp conf\'')
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
            dataRecs = sample_manager.getData(sample)
            for dataRec in dataRecs:
                print('\t' + str(dataRec))

@main.command()
@click.option('--name',prompt='NAME',help='unique name for the sample')
@click.option('--project',prompt='PROJECT',help='unique name of the project')
@click.option('--modify/--no-modify', default=False, help='overwrite fields in an existing record')
@click.argument('metadata', nargs=-1)
def save_sample(name, project,modify, metadata):
    metadataDict = {}
    for kvstr in metadata:
        k, v = kvstr.split('=')
        metadataDict[k] = v
    sample = mupdb.Sample(name=name,
                    project_name=project,
                    metadata=metadataDict)
    sample = sample.save(modify=modify)
    print(sample)

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

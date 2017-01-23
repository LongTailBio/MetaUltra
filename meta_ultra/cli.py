# -*- coding: utf-8 -*-

import click
import meta_ultra.refs as refs
import meta_ultra.conf_builder as conf_builder
import meta_ultra.pipeline_runner as pipeline_runner
import os.path
import json

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
@click.option('--pairs/--single', default=False, help='Reads are pairwise')
@click.argument('samples', nargs=-1)
def new_conf(pairs,samples):
    myconf = conf_builder.build_conf(samples,pairs=pairs)
    print( json.dumps(myconf, sort_keys=True, indent=4))

@main.command()
@click.option('--dryrun/--normal',default=False,help='Print schedule but dont run anything')
@click.option('--jobs',default=1,help='Number of jobs to run')
@click.option('--conf',prompt='CONF FILE', help='Conf file, can be generated using \'pmp conf\'')
def run(dryrun,jobs,conf):
    if not os.path.isfile(conf):
        sys.stderr.write('Conf file {} not found. Exiting...'.format(conf))
        sys.exit(1)
        
    pipeline_runner.run(conf,dry_run=dryrun,njobs=jobs)

if __name__ == "__main__":
    main()

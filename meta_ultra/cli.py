# -*- coding: utf-8 -*-

import click
import refs
import conf

@click.group()
def main():
    pass

@main.command()
@click.option('--tool', prompt='TOOL', help='The tool that the reference is intended to be used with')
@click.option('--name', default=None, help='Reference Name')
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
    conf.build_conf(samples,pairs=pairs)

@main.command()
@click.option('--conf',prompt='CONF FILE', help='Conf file, can be generated using \'pmp conf\'')
def run(conf):
    pass

if __name__ == "__main__":
    main()

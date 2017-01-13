# -*- coding: utf-8 -*-

import click


@click.group()
def main():
    pass

@main.command()
@click.option('--tool', prompt='TOOL', help='The tool that the reference is intended to be used with')
@click.option('--name', default=None, help='Reference Name')
@click.option('--ref', prompt='FILE PATH', help='Location of reference')
def add_reference(tool,name,ref):
    pass

@main.command()
def list_references():
    pass

@main.command()
def conf():
    pass

@main.command()
@click.option('--conf',prompt='CONF FILE', help='Conf file, can be generated using \'pmp conf\'')
def run(conf):
    pass

if __name__ == "__main__":
    main()

from meta_ultra.user_input import *
import meta_ultra.api as api
from .cli import main
import click
import meta_ultra.conf_builder as conf_builder
from tempfile import NamedTemporaryFile
import json
import subprocess as sp
import meta_ultra.config as config
import os

@main.group()
def edit():
    pass
    

@edit.command(name='conf')
@click.option('--raw/--no-raw',default=False,help='edit in a text editor')
@click.argument('name',nargs=1)
def cli_editConf(name,raw=False):
    conf = api.getConf(name)
    if raw:
        tf = NamedTemporaryFile(mode='w',dir=config.get_config(path=True), delete=False)
        confDict = json.dumps(conf.confDict, indent=4, sort_keys=True)
        tf.write(confDict)
        tf.close()
        outcode = sp.call('{} {}'.format(os.environ['EDITOR'], tf.name), shell=True)
        if outcode == 0:
            with open(tf.name) as edited:
                editedDict = json.load(edited)
                api.saveConf(conf.name, editedDict, modify=True)
        os.remove(tf.name)
    return api.getConf(name)

def addConf(name=None, useDefaults=None, fineControl=None):
    if not name:
        name = UserInputNoDefault('What is the name of this conf?').resolve()
    if not fineControl and useDefaults is None:
        useDefaults = BoolUserInput('Accept all default parameters for this conf?', False).resolve()
    if fineControl is None and not useDefaults:
        fineControl = BoolUserInput('Control absolutely every aspect of this conf?', False).resolve()

    return conf_builder.buildNewConf(name, useDefaults=useDefaults, fineControl=fineControl)
    
    
@edit.command(name='remote')
@click.argument('name', nargs=1)
@click.argument('url', nargs=1)
def editRemote(name, url):
    api.editRemote(name, url)

    

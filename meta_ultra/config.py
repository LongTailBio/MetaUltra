import os.path
import os
from tinydb import TinyDB
import sys
from enum import Enum
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


lib_root = os.path.dirname(__file__)

pipeline_dir = os.path.join( lib_root, 'pipelines/')
snake_file = lambda : os.path.join( pipeline_dir, 'all.snkmk')

def snakemake_static_conf_file():
    repo = get_repo(path=True)
    repo = os.path.dirname(repo)
    staticConf = os.path.join( repo,'snakemake_static_config.json')
    staticConf = os.path.abspath( staticConf)
    return staticConf

def cluster_wrapper():
    customWrapper = os.path.join( os.path.dirname(get_repo(path=True)),
                                  'cluster_submission_wrapper_script.py')
    if os.path.exists(customWrapper):
        return customWrapper
    defaultWrapper = os.path.join( pipeline_dir, 'default_cluster_submission_wrapper_script.py')
    return defaultWrapper

    
mu_repo_dir = '.mu'
mu_repo_path = os.path.join(mu_repo_dir,'mu_repo.tinydb.json')

mu_config_dir = os.path.join( os.environ['HOME'], '.muconfig')
if 'MU_CONFIG' in os.environ:
    mu_config_dir = os.environ['MU_CONFIG']

def get_config(path=False):
    configPath = os.path.join( mu_config_dir, 'mu_config.tinydb.json')
    if path:
        return os.path.dirname(configPath)
    return TinyDB( configPath)


        
def get_repo(dir='.', path=False):
    dir = os.path.abspath(dir)
    if mu_repo_dir in os.listdir(dir):
        mu_db = os.path.join(dir,mu_repo_path)
        if path:
            return mu_db
        mu_db = TinyDB(mu_db)
        return mu_db
    else:
        # recurse up
        up = os.path.dirname(dir)
        if up == dir:
            # top, fail
            sys.stderr.write('No MetaUltra database found. Exiting.\n')
            sys.exit(1)
        else:
            return get_repo(up)

db_conf_table = lambda : get_config().table('conf_table')        
db_mu_config_remotes = lambda : get_config().table('mu_config_remotes')

db_module_table = lambda : get_repo().table('module_table')
db_sample_table = lambda : get_repo().table('sample_table')
db_project_table = lambda : get_repo().table('project_table')
db_data_table = lambda : get_repo().table('data_table')
db_experiment_table = lambda : get_repo().table('experiment_table')
db_result_table = lambda : get_repo().table('result_table')
db_project_result_table = lambda : get_repo().table('project_result_table')


def canon_tool(toolName):
    return toolName.lower()

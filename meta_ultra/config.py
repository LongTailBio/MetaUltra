import os.path
import os
from tinydb import TinyDB
import sys
from enum import Enum
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


lib_root = os.path.dirname(__file__)

pipeline_dir = os.path.join( lib_root, 'pipelines/')
snake_file = os.path.join( pipeline_dir, 'all.snkmk')
snakemake_static_conf_file = lambda : os.path.abspath( os.path.join( os.path.dirname(get_repo()),'snakemake_static_config.json'))

def cluster_wrapper():
    customWrapper = os.path.join( os.path.dirname(get_repo()), 'cluster_submission_wrapper_script.py')
    if customWrapper.is_file():
        return customWrapper
    defaultWrapper = os.path.join( pipeline_dir, 'default_cluster_submission_wrapper_script.py')
    return defaultWrapper

    
mu_repo_dir = '.mu'
mu_repo_path = os.path.join(mu_repo_dir,'mu_repo.tinydb.json')

mu_config_dir = os.path.join( os.environ['HOME'], '.muconfig')
if 'MU_CONFIG' in os.environ:
    mu_config_dir = os.environ['MU_CONFIG']
get_config = lambda : TinyDB( os.path.join( mu_config_dir, 'mu_config.tinydb.json'))


        
def get_repo(dir='.'):
    dir = os.path.abspath(dir)
    if mu_dir in os.listdir(dir):
        mu_db = TinyDB( os.path.join(dir,mu_db_path))
        return mu_db
    else:
        # recurse up
        up = os.path.dirname(dir)
        if up == dir:
            # top, fail
            sys.stderr.write('No MetaUltra database found. Exiting.\n')
            sys.exit(1)
        else:
            return get_db(up)

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

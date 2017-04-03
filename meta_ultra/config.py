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
cluster_wrapper = os.path.join( pipeline_dir, 'cluster_submission_wrapper_script.py')
snakemake_static_conf_file = lambda : os.path.abspath( os.path.join(get_mu_dir(),'snakemake_static_config.json'))


mu_dir = '.mu'
mu_db_path = os.path.join(mu_dir,'mudb')


def get_mu_dir(dir='.'):
    dir = os.path.abspath(dir)
    if mu_dir in os.listdir(dir):
        return os.path.join(dir, mu_dir)
    else:
        # recurse up
        up = os.path.dirname(dir)
        if up == dir:
            # top, fail
            sys.stderr.write('No MetaUltra database found. Exiting.\n')
            sys.exit(1)
        else:
            return get_mu_dir(up)


        
def get_db(dir='.'):
    global cached_mu_db
    
    try:
        if cached_mu_db != None:
            return cached_mu_db
    except NameError:
        pass
    
    dir = os.path.abspath(dir)
    if mu_dir in os.listdir(dir):
        mu_db = TinyDB( os.path.join(dir,mu_db_path))

        cached_mu_db = MuDB(mu_db)
        return cached_mu_db
    else:
        # recurse up
        up = os.path.dirname(dir)
        if up == dir:
            # top, fail
            sys.stderr.write('No MetaUltra database found. Exiting.\n')
            sys.exit(1)
        else:
            return get_db(up)

class MuDB:
    def __init__(self, tinyDB):
        self.tinyDB = tinyDB
        self.tableCache = {}

    def table(self, tblName):
#        return self.tinyDB.table(tblName)
        if tblName in self.tableCache:
            return self.tableCache[tblName]
        tbl = self.tinyDB.table(tblName)
        self.tableCache[tblName] = tbl
        return tbl

        
db_mu_config_remotes = lambda : get_db().table('mu_config_remotes')
db_module_table = lambda : get_db().table('module_table')
db_sample_table = lambda : get_db().table('sample_table')
db_project_table = lambda : get_db().table('project_table')
db_data_table = lambda : get_db().table('data_table')
db_experiment_table = lambda : get_db().table('experiment_table')
db_conf_table = lambda : get_db().table('conf_table')
db_result_table = lambda : get_db().table('result_table')


def canon_tool(toolName):
    return toolName.lower()

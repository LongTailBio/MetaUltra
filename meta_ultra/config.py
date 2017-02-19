import os.path
import os


lib_root = os.path.dirname(__file__)

ref_file = os.path.join( lib_root, 'references')
pipeline_dir = os.path.join( lib_root, 'pipelines/')
snake_file = os.path.join( pipeline_dir, 'all.snkmk')
cluster_wrapper = os.path.join( lib_root, 'cluster_wrapper_script.py')

mup_root = os.environ['MUP_ROOT']

db_file = os.environ['MUP_DB']

db_module_table = 'module_table'
db_sample_table = 'sample_table'
db_data_table = 'data_table'
db_experiment_table = 'experiment_table'
db_conf_table = 'conf_table'
db_result_table = 'result_table'


def canon_tool(toolName):
    return toolName.lower()

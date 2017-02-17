import os.path
import os


lib_root = os.path.dirname(__file__)

ref_file = os.path.join( lib_root, 'references')
snake_file = os.path.join( lib_root, 'all.snkmk')
cluster_wrapper = os.path.join( lib_root, 'cluster_wrapper_script.py')

mup_root = os.environ['MUP_ROOT']

db_file = os.environ['MUP_DB']

db_reference_table = 'reference_table'
db_tool_table = 'tool_table'
db_sample_table = 'sample_table'
db_data_table = 'data_table'
db_experiment_table = 'experiment_table'
db_conf_table = 'conf_table'
db_result_table = 'result_table'


def canon_tool(toolName):
    return toolName.lower()

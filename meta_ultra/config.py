import os.path

lib_root = os.path.dirname(__file__)

ref_file = os.path.join( lib_root, 'references')
snake_file = os.path.join( lib_root, 'all.snkmk')
cluster_wrapper = os.path.join( lib_root, 'cluster_wrapper_script.py')

db_file = os.path.join(lib_root, 'db_file.json')
db_reference_table = 'reference_table'


def canon_tool(toolName):
    return toolName.lower()

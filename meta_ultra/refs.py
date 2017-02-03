from tinydb import TinyDB, Query
import meta_ultra.config as config 

def add_reference(tool,name,path):
    db = TinyDB( config.db_file)
    refs = db.table(config.db_reference_table)
    refs.insert({
        'tool': config.canon_tool(tool),
        'name': name,
        'path' : path
    })

def list_references():
    print('Tool\tName\tPath')
    db = TinyDB( config.db_file)
    refs = db.table(config.db_reference_table)
    for ref in refs.all():
        print('{}\t{}\t{}'.format(ref['tool'], ref['name'], ref['path']))

def remove_reference(eid):
    refTbl = TinyDB(config.db_file).table(config.db_reference_table)
    refTbl.remove(eids=[eid])
    
class Reference:
     def __init__(self, tool, name, path):
         self.tool = tool
         self.name = name
         self.path = path

def get_references(tool=None):
    refs = []
    refTbl = TinyDB(config.db_file).table(config.db_reference_table)
    for ref in refTbl.all():
        if config.canon_tool(tool) == ref['tool']: 
            refs.append( Reference( ref['tool'], ref['name'], ref['path']))

    return(refs)

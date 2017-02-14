from tinydb import TinyDB, Query
import meta_ultra.config as config 

def add_tool(toolName,version,excPath):
    db = TinyDB( config.db_file)
    tools = db.table(config.db_tool_table)
    
    tools.insert({
        'name': config.canon_tool(toolName),
        'version': version,
        'exc' : excPath
    })

def list_tools():
    print('eid\tName\tVersion\tExecutable')
    db = TinyDB( config.db_file)
    tools = db.table(config.db_tool_table)
    for tool in tools.all():
        print('{}\t{}\t{}\t{}'.format(tool.eid, tool['name'], tool['version'], tool['exc']))

def remove_tool(eid):
    toolTbl = TinyDB(config.db_file).table(config.db_tool_table)
    toolTbl.remove(eids=[eid])
        
class Tool:
     def __init__(self, name, version, exc):
         self.name = name
         self.version = version
         self.exc = exc

def get_tools(name=None):
    tools = []
    toolTbl = TinyDB(config.db_file).table(config.db_tool_table)
    for tool in toolTbl.all():
        if config.canon_tool(name) == config.canon_tool(tool['name']): 
            tools.append( Tool( tool['name'], tool['version'], tool['exc'] ))

    return(tools)

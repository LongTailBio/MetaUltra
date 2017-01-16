
import meta_ultra.config as config 

def add_reference(tool,name,path):
    with open(config.ref_file,'a') as rf:
        rf.write('{}\t{}\t{}'.format(tool,name,path))

def list_references():
    print('Tool\tName\tPath')
    print(open(config.ref_file).read())

class Reference:
     def __init__(self, tool, name, path):
         self.tool = tool
         self.name = name
         self.path = path

def get_references(tool=None):
    refs = []
    with open(config.ref_file) as rf:
        for line in rf:
            mytool, name, path = line.strip().split()
            if tool and mytool.lower() != tool.lower():
                continue
            ref = Reference(mytool, name, path)
            refs.append(ref)
    return(refs)

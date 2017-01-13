
import config 

def add_reference(tool,name,path):
    with open(config.ref_file,'a') as rf:
        rf.write('{}\t{}\t{}'.format(tool,name,path))

def list_references():
    print('Tool\tName\tPath')
    print(open(config.ref_file).read())






class MUConfig:
    '''
    MUConfig is an object that represents higher level variables than repo

    Currently there are three levels to config: default, user and repo. Any setting in
    a repo will override the analogous setting in user or default. Any setting in user 
    will override default. 

    This is seperate from program_config.py which holds various static values 
    for the program itself.

    Values MUConfig stores, all values depend on the level and working dir:
     - pipeline configuration

    '''

    def __init__(self):
        pass

class PipelineConfig:
    '''
    PipelineConfig is a part of MUConfig that handles any configuration 
    related to pipelines.

    Values PipelineConfig is responsible for:
     - what pipelines are available
     - any configurations each pipeline requires
     - custom run commands (useful for cluster systems)
    '''

    def __init__(self):

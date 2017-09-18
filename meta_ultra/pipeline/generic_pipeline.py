


class GenericPipeline:
    '''
    The pipeline class represents the instantiation of an underlying pipeline.


    The class itself defines features that do not change for a given version of
    the pipeline, such as:
     - human readable name of the pipeline
     - version number installed 
     - result types the pipeline defines (or inherits from dependecies)
     - sample types the pipeline defines (or inherits from dependecies)
     - the endpoints (submodules) that the pipline provides

    Each pipeline object provides features that change depending on how the 
    pipeline is going to be used, such as:
     - What endpoints (submodules) are going to be run
     - a function to setup (install) the pipeline
     - a function to run the pipeline on provided records

    '''
    
    
    def __init__(self, endpts=set()):
        self.endpts = endpts


    def process(self, records, repo):
        '''
        Do whatever it is your pipeline does with the 
        records and repo provided.
        
        There really are no limits to what you're allowed 
        to do though you're encouraged to follow certain 
        conventions (such as recording new results in 
        the repo). 

        Your pipeline can ask for user input here but in most cases 
        it should not. If there are values a user needs to set to run 
        pipeline those should be set in the relevant pipeline_config
        during setup. 
        '''
        raise NotImplementedError()

    def setup(self, pipelineConfig, installLevel):
        '''
        This will be run when your pipeline is installed for a user
        or into a new repo. 'installLevel' will tell you the highest
        level the pipeline is being installed at, either 'user' or 'repo'
        currently.

        Your pipeline is free to ask for user input via the CLI in this
        function.
        '''
        
        raise NotImplementedError()

    
    def addEndPoint(self, endpt):
        self.endpts.add(endpt)

    def addEndPoints(self, endpts):
        for endpt in endpts:
            self.addEndPoint( endpt)
        
    def requestedEndPoints(self):
        return self.endpts
        
    def depends(self):
        # the list of dependencies can change based on the requested end pts
        return None, None

    @classmethod
    def basename():
        return 'generic_pipeline'

    @classmethod
    def version():
        raise NotImplementedError()
    
    @classmethod
    def name():
        return '{}:{}'.format( )
        
    @staticmethod
    def resultTypes():
        raise NotImplementedError()

    @staticmethod
    def sampleTypes():
        raise NotImplementedError()

    @staticmethod
    def allEndPoints():
        raise NotImplementedError()
        




class GenericPipeline:

    def __init__(self, endpts=set()):
        self.endpts = endpts


    def process(self, records, repo):
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

    @staticmethod
    def name():
        return 'generic_pipeline'

    @staticmethod
    def resultTypes():
        raise NotImplementedError()

    @staticmethod
    def sampleTypes():
        raise NotImplementedError()

    @staticmethod
    def allEndPoints():
        raise NotImplementedError()
        

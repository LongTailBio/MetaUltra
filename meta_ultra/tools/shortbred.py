import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.tools import *
from meta_ultra.conf_builder import *
                		
class ShortBredSet( ToolSet):
        def __init__(self, **kwargs):
                super(ShortBredSet, self).__init__(ShortBredSet.toolSetName(), **kwargs)
                self.ext = self.params['ext']
                self.time = self.params['time']
                self.ram = self.params['ram']

        def buildConf(self, confBuilder):
                shortbred = confBuilder.add_tool(setName.upper())
	        shortbred.add_field('EXT', self.ext)
                shortbred.add_field('EXC',
			            UserChoice('ShortBred Version',
					            self.excFiles))),
	        
                shortbred.add_field('DBS',
			            UserMultiChoice('ShortBred References',
					            self.refs))),
	        shortbred.add_field('THREADS',
			            UserInput('\tHow many threads would you like for shortbred',
				              conf.get_global_field('THREADS'),
				              type=int,
                                    	      fineControlOnly=True))
	        shortbred.add_field('TIME',
			            UserInput('\tHow many hours does shortbred need',
				              self.time,
				              type=int,
                                              fineControlOnly=True))
	        shortbred.add_field('RAM',
			            UserInput('\tHow many GB of RAM does shortbred need per thread',
				              self.ram,
				              type=int,
                                    	      fineControlOnly=True))

        @staticmethod
        def toolSetName():
                return 'shortbred'
                
toolsets.append(ShortBredSet)

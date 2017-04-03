import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *

class CountClassifiedModule( Module):
	def __init__(self, **kwargs):
		super(CountClassifiedModule, self).__init__(**kwargs)		

	def buildConf(self, conf):
		countClass = conf.addModule('COUNT_CLASSIFIED')
		if not countClass:
			return
		
		countClass.add_field('EXC',
				     UserChoice('Count Script',
						self.tools,
						new=lambda :self.askUserForTool('count_script')
				     ))

		
	@staticmethod
	def moduleName():
		return 'count_classified'

		
modules.append(CountClassifiedModule)

import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *


class BlastNModule( Module):
	def __init__(self, **kwargs):
		super(BlastNModule, self).__init__(**kwargs)		
		

	def buildConf(self, confBuilder):
		blastn = confBuilder.addModule(self.moduleName().upper())
		if not blastn:
			return
		
		blastn.add_field('EXC',
				  UserChoice('BlastN',
					     self.tools,
					     new=lambda :self.askUserForTool('blastn')
				  ))

		
	@staticmethod
	def moduleName():
		return 'blastn'

		
modules.append(BlastNModule)

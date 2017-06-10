import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *


class BWAModule( Module):
	def __init__(self, **kwargs):
		super(BWAModule, self).__init__(**kwargs)		
		

	def buildConf(self, confBuilder):
		bwa = confBuilder.addModule(self.moduleName().upper())
		if not bwa:
			return
		
		bwa.add_field('EXC',
				  UserChoice('BWA',
					     self.tools,
					     new=lambda :self.askUserForTool('bwa')
				  ))
	@staticmethod
	def moduleName():
		return 'bwa'

		
modules.append(BWAModule)

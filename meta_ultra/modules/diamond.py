import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.conf_builder import *


class DiamondModule( Module):
	def __init__(self, **kwargs):
		super(DiamondModule, self).__init__(**kwargs)		
		

	def buildConf(self, confBuilder):
		diamond = confBuilder.addModule(self.moduleName().upper())
		diamond.add_field('EXC',
				  UserChoice('Diamond',
					     self.tools,
					     new=lambda :self.askUserForTool('diamond')
				  ))
		
	@staticmethod
	def moduleName():
		return 'diamond'

		
modules.append(DiamondModule)
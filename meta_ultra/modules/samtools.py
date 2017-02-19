import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.conf_builder import *


class SamtoolsModule( Module):
	def __init__(self, **kwargs):
		super(SamtoolsModule, self).__init__(**kwargs)		
		

	def buildConf(self, confBuilder):
		samtools = confBuilder.addModule(self.moduleName().upper())
		samtools.add_field('EXC',
				  UserChoice('Samtools',
					     self.tools,
					     new=lambda :self.askUserForTool('samtools')
				  ))
		
	@staticmethod
	def moduleName():
		return 'samtools'

		
modules.append(SamtoolsModule)

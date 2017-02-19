import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.conf_builder import *


class Bowtie2Module( Module):
	def __init__(self, **kwargs):
		super(Bowtie2Module, self).__init__(**kwargs)		
		

	def buildConf(self, confBuilder):
		bowtie2 = confBuilder.addModule(self.moduleName().upper())
		bowtie2.add_field('EXC',
				  UserChoice('Bowtie2',
					     self.tools,
					     new=lambda :self.askUserForTool('bowtie2')
				  ))
		
	@staticmethod
	def moduleName():
		return 'bowtie2'

		
modules.append(Bowtie2Module)

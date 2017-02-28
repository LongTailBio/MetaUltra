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
	@classmethod
	def worksForDataType(ctype, dataType):
		dataType = DataType.asDataType(dataType)
		allowed = [ DataType.WGS_DNA_SEQ_SINGLE_END, DataType.WGS_DNA_SEQ_PAIRED_END]
		return dataType in allowed
	
		
	@staticmethod
	def moduleName():
		return 'samtools'

		
modules.append(SamtoolsModule)

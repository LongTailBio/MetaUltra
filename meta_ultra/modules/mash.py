import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *


class MashModule( Module):
	def __init__(self, **kwargs):
		super(MashModule, self).__init__(**kwargs)		

	def buildConf(self, conf):
		mash = conf.addModule('MASH')
		if not mash:
			return
		
		mash.add_field('EXC',
			       UserChoice('Mash (kmer minhash distances)',
					  self.getToolsOfType('mash'),
					  new=lambda :self.askUserForTool('mash')
			       ))
		mash.add_field('DBS',
			       UserMultiChoice('ShortBred References',
					       self.refs,
					       new=lambda : self.askUserForRef('mash')
			       ))
		mash.add_field('DIST_SCRIPT',
			       UserChoice('Script to turn mash dists into useful json',
					  self.getToolsOfType('mash-dist-script'),
					  new=lambda :self.askUserForTool('mash-dist-script')
			       ))

	@classmethod
	def worksForDataType(ctype, dataType):
		dataType = DataType.asDataType(dataType)
		allowed = [ DataType.WGS_DNA_SEQ_SINGLE_END, DataType.WGS_DNA_SEQ_PAIRED_END]
		return dataType in allowed
		
	@staticmethod
	def moduleName():
		return 'mash'

		
modules.append(MashModule)
	

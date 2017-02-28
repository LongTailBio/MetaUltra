import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.conf_builder import *
from meta_ultra.data_type import *

class ShortBredModule( Module):
	def __init__(self, **kwargs):
		super(ShortBredModule, self).__init__(**kwargs)		
		self.ext = self.getParamOrDefault('ext', 'shortbred.tsv')
		self.time = self.getParamOrDefault('time', 1)
		self.ram = self.getParamOrDefault('ram', 4)

	def expectedOutputFiles(self, dataRec):
		sname = dataRec.sampleName
		dname = dataRec.name
		return ['{}.{}.{}'.format(sname,dname,self.ext)]
	
	def buildConf(self, confBuilder):
		shortbred = confBuilder.addModule(self.moduleName().upper())

		shortbred.add_field('EXT', self.ext)
		shortbred.add_field('EXC',
				    UserChoice('ShortBred Quantify',
					       self.tools,
					       new=lambda :self.askUserForTool('shortbred_quantify')
				    ))
		tool = shortbred.get_field('EXC')
		shortbred.set_field('EXC', tool['filepath'])
		shortbred.set_field('VERSION', tool['version'])
		
		shortbred.add_field('DBS',
				    UserMultiChoice('ShortBred References',
						    self.refs,
						    new=lambda : self.askUserForRef('shortbred_quantify')
				    ))
		dbs = shortbred.get_field('DBS')
		dbPaths = []
		for db in dbs:
			dbPaths.append(db['filepath'])
		shortbred.set_field('DBS', dbPaths)
		
		shortbred.add_field('THREADS',
				    UserInput('\tHow many threads would you like for shortbred',
					      confBuilder.get_global_field('THREADS'),
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

	@classmethod
	def worksForDataType(ctype, dataType):
		dataType = DataType.asDataType(dataType)
		allowed = [ DataType.WGS_DNA_SEQ_SINGLE_END, DataType.WGS_DNA_SEQ_PAIRED_END]
		return dataType in allowed
		
	@staticmethod
	def moduleName():
		return 'shortbred'

	
modules.append(ShortBredModule)

import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.conf_builder import *


class MicrobeCensusModule( Module):
	def __init__(self, **kwargs):
		super(MicrobeCensusModule, self).__init__(**kwargs)		
		self.ext = self.getParamOrDefault('ext', 'mic_census.txt')
		self.time = self.getParamOrDefault('time', 1)
		self.ram = self.getParamOrDefault('ram', 10)

	def expectedOutputFiles(self, dataRec):
		sname = dataRec.sampleName
		dname = dataRec.name
		return ['{}.{}.{}'.format(sname, dname, self.ext)]
		
	def buildConf(self, conf):
		micCensus = conf.addModule('MICROBE_CENSUS')
		micCensus.add_field('EXC',
				    UserChoice('Microbe Census',
					       self.tools,
					       new=lambda :self.askUserForTool('microbe_census')
				    ))
		micCensus.add_field('EXT', self.ext)
		micCensus.add_field('THREADS',
				    UserInput('\tHow many threads would you like for MicrobeCensus',
					      conf.get_global_field('THREADS'),
					      type=int,
					      fineControlOnly=True
				    ))
		micCensus.add_field('TIME',
				    UserInput('\tHow many hours does MicrobeCensus need',
					      self.time,
					      type=int,
					      fineControlOnly=True
				    ))
		micCensus.add_field('RAM',
				    UserInput('\tHow many GB of RAM does MicrobeCensus need per thread',
					      self.ram,
					      type=int,
					      fineControlOnly=True
				    ))
	@classmethod
	def worksForDataType(ctype, dataType):
		dataType = DataType.asDataType(dataType)
		allowed = [ DataType.DNA_SEQ_SINGLE_END, DataType.DNA_SEQ_PAIRED_END]
		return dataType in allowed

	@staticmethod
	def moduleName():
		return 'microbe_census'

		
modules.append(MicrobeCensusModule)

	

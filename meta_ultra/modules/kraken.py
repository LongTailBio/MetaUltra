import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *

class KrakenModule( Module):
	def __init__(self, **kwargs):
		super(KrakenModule, self).__init__(**kwargs)		
		self.rawExt = self.getParamOrDefault('raw_ext', 'raw_kraken.tsv')
		self.mpaExt = self.getParamOrDefault('mpa_ext', 'mpa_kraken.tsv')
		self.time = self.getParamOrDefault('time', 1)
		self.ram = self.getParamOrDefault('ram', 4)
		self.mpaTime = self.getParamOrDefault('mpa_time', 1)
		self.mpaRam = self.getParamOrDefault('mpa_ram', 10)
		
	def expectedOutputFiles(self, dataRec):
		sname = dataRec.sampleName
		dname = dataRec.name
		rawName = '{}.{}.{}'.format(sname, dname, self.rawExt)
		mpaName = '{}.{}.{}'.format(sname, dname, self.mpaExt)
		return [rawName, mpaName]
		
	def buildConf(self, conf):
		kraken = conf.addModule('KRAKEN')
		if not kraken:
			return
		
		kraken.add_field('RAW_EXT', self.rawExt)
		kraken.add_field('MPA_EXT', self.mpaExt)
		kraken.add_field('EXC',
				 UserChoice('Kraken',
					    self.getToolsOfType('kraken'),
					    new=lambda : self.askUserForTool('kraken')
				 ))
		kraken.add_field('MPA_EXC',
				 UserChoice('Kraken MPA report generator',
					    self.getToolsOfType('kraken-mpa-report'),
					    new=lambda : self.askUserForTool('kraken-mpa-report')
				 ))
		kraken.add_field('DB',
				 UserChoice('Kraken DB',
					    self.refs,
					    new=lambda : self.askUserForRef('Kraken DB')
				 )),
		kraken.add_field('THREADS',
				 UserInput('\tHow many threads would you like for kraken',
					   conf.get_global_field('THREADS'),
					   type=int,
					   fineControlOnly=True
				 ))
		kraken.add_field('TIME',
				 UserInput('\tHow many hours does kraken need',
					   self.time,
					   type=int,
					   fineControlOnly=True
				 ))
		kraken.add_field('MPA_TIME', self.mpaTime)
		kraken.add_field('RAM',
				 UserInput('How much RAM does Kraken need per thread',
					   self.ram,
					   type=int,
					   fineControlOnly=True
				 ))
		kraken.add_field('MPA_RAM', self.mpaRam)

	@classmethod
	def worksForDataType(ctype, dataType):
		dataType = DataType.asDataType(dataType)
		allowed = [ DataType.WGS_DNA_SEQ_SINGLE_END, DataType.WGS_DNA_SEQ_PAIRED_END]
		return dataType in allowed
	
		
	@staticmethod
	def moduleName():
		return 'kraken'


	
		
modules.append(KrakenModule)

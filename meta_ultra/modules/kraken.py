import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.conf_builder import *


class KrakenModule( Module):
	def __init__(self, **kwargs):
		super(KrakenModule, self).__init__(**kwargs)		
		self.rawExt = self.getParamOrDefault('raw_ext', '.raw_kraken.tsv')
		self.mpaExt = self.getParamOrDefault('mpa_ext', '.mpa_kraken.tsv')
		self.time = self.getParamOrDefault('time', 1)
		self.ram = self.getParamOrDefault('ram', 4)
                self.mpaTime = self.getParamOrDefault('mpa_time', 1)
                self.mpaRam = self.getParamOrDefault('mpa_ram', 10)
                
	def buildConf(self, conf):
                kraken = conf.add_tool('KRAKEN')
	        kraken.add_field('RAW_EXT', self.rawExt)
	        kraken.add_field('MPA_EXT', self.mpaExt)
	        kraken.add_field('EXC',
			         UserChoice('Kraken',
				            [tool for tool in tools if tool.name.lower() == 'kraken'],
                                            new=lambda : self.askUserForTool('kraken')
                                 ))
	        kraken.add_field('MPA_EXC',
			         UserChoice('Kraken MPA report generator',
				            [tool for tool in tools if tool.name.lower() == 'kraken-mpa-report'],
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

	@staticmethod
	def moduleName():
		return 'kraken'

		
modules.append(KrakenModule)

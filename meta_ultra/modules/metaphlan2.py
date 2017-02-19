import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.conf_builder import *


class Metaphlan2Module( Module):
	def __init__(self, **kwargs):
		super(Metaphlan2Module, self).__init__(**kwargs)		
		self.ext = self.getParamOrDefault('ext', 'metaphlan2.tsv')
		self.time = self.getParamOrDefault('time', 1)
		self.ram = self.getParamOrDefault('ram', 4)

	def buildConf(self, conf):
		metaphlan2 = conf.add_tool('METAPHLAN2')
                metaphlan2.add_field('EXC',
                                     UserChoice('MetaPhlAn2 Executable',
                                                self.tools,
                                                new=lambda :self.askUserForTool('metaphlan2')
                                     ))
	        metaphlan2.add_field('REF',
                                     UserChoice('MetaPhlAn2 Reference',
                                                self.refs,
                                                new=lambda :self.askUserForRef('metaphlan2')
                                     ))
	        metaphlan2.add_field('THREADS',
			             UserInput('\tHow many threads would you like for metaphlan2',
				               conf.get_global_field('THREADS'),
                                               type=int,
                                               fineControlOnly=True
                                     ))
	        metaphlan2.add_field('TIME',
			             UserInput('\tHow many hours does metaphlan2 need',
				               1,
				               type=int,
                                               fineControlOnly=True
                                     ))
	        metaphlan2.add_field('RAM',
			             UserInput('\tHow many GB of RAM does metaphlan2 need per thread',
				               self.ram,
				               type=int,
                                               fineControlOnly=True
                                     ))
                metaphlan2.add_field('EXT', self.ext)

	@staticmethod
	def moduleName():
		return 'metaphlan2'

		
modules.append(Metaphlan2Module)

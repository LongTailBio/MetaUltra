import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.data_type import *

class FilterHostModule( Module):
	def __init__(self, **kwargs):
		super(FilterHostModule, self).__init__(**kwargs)		
		self.time = self.getParamOrDefault('time', 20)
		self.ram = self.getParamOrDefault('ram', 5)
	
	def buildConf(self, confBuilder):
		filterHost = confBuilder.addModule(self.moduleName().upper())
		if not filterHost:
			return
		
		filterHost.add_field('DB',
				    UserChoice('Host Genome BT2 Index',
					       self.refs,
					       new=lambda : self.askUserForRef('host_genome_bt2_index')
				    ))

		filterHost.add_field('TIME',
				    UserInput('\tHow many hours are necessary to filter host reads',
					      self.time,
					      type=int,
					      fineControlOnly=True))                
		filterHost.add_field('THREADS',
				    UserInput('\tHow many threads would you like to filter host reads',
					      confBuilder.get_global_field('THREADS'),
					      type=int,
					      fineControlOnly=True))
		filterHost.add_field('RAM',
				    UserInput('\tHow many GB of RAM per thread are encessary to filter host reads',
					      self.ram,
					      type=int,
					      fineControlOnly=True))

		
	@staticmethod
	def moduleName():
		return 'filter_host'

	
modules.append(FilterHostModule)

import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.data_type import *

class Humann2Module( Module):
	def __init__(self, **kwargs):
		super(Humann2Module, self).__init__(**kwargs)		
		self.time = self.getParamOrDefault('time', 1)
		self.ram = self.getParamOrDefault('ram', 4)
		self.dmnd_time = self.getParamOrDefault('dmnd_time', 1)
		self.dmnd_ram = self.getParamOrDefault('dmnd_ram',5)
	
	def buildConf(self, confBuilder):
		humann2 = confBuilder.addModule(self.moduleName().upper())
		if not humann2:
			return
		
		humann2.add_field('EXC',
				    UserChoice('Humann2',
					       self.tools,
					       new=lambda :self.askUserForTool('humann2')
				    ))
		
		humann2.add_field('DB',
				    UserChoice('Humann2 Reference',
					       self.refs,
					       new=lambda : self.askUserForRef('humann2_diamond_db')
				    ))

		# Diamond
		humann2.add_field('DMND_THREADS',
				    UserInput('\tHow many threads would you like for humann2',
					      2*int(confBuilder.get_global_field('THREADS')),
					      type=int,
					      fineControlOnly=True))
		humann2.add_field('DMND_TIME',
				    UserInput('\tHow many hours does diamond (in humann2) need',
					      self.dmnd_time,
					      type=int,
					      fineControlOnly=True))		    
		humann2.add_field('DMND_RAM',
				    UserInput('\tHow many GB of RAM does humann2 need per thread',
					      self.dmnd_ram,
					      type=int,
					      fineControlOnly=True))
		# humann2
		humann2.add_field('THREADS',
				    UserInput('\tHow many threads would you like for humann2',
					      confBuilder.get_global_field('THREADS'),
					      type=int,
					      fineControlOnly=True))
		humann2.add_field('TIME',
				    UserInput('\tHow many hours does humann2 need',
					      self.time,
					      type=int,
					      fineControlOnly=True))		    

		humann2.add_field('RAM',
				    UserInput('\tHow many GB of RAM does humann2 need per thread',
					      self.ram,
					      type=int,
					      fineControlOnly=True))

		
	@staticmethod
	def moduleName():
		return 'humann2'

	
modules.append(Humann2Module)

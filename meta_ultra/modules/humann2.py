import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.conf_builder import *


class Humann2Module( Module):
	def __init__(self, **kwargs):
		super(Humann2Module, self).__init__(**kwargs)		

		self.time = self.getParamOrDefault('time', 2)
		self.ram = self.getParamOrDefault('ram', 10)

                self.dmndTime = self.getParamOrDefault('dmnd_time', 5)
                self.dmndRam = self.getParamOrDefault('dmnd_ram', 10)

        def buildConf(self, conf):
                humann2 = conf.add_tool('HUMANN2')
	        humann2.add_field('DB',
			          RefChoice('Humann2 DB',
				            get_references(tool='humann2'))),
	        humann2.add_field('DMND_TIME',
			          UserInput('\tHow many hours does diamond (as a part of Humann2) need',
				            self.dmndTime,
				            type=int,
                                            fineControlOnly=True,
                                  ))
	        humann2.add_field('DMND_THREADS',
			          UserInput('\tHow many threads would you like for diamond (as part of HumanN2)',
				            2*conf.get_global_field('THREADS'),
				            type=int,
                                            fineControlOnly=True,
                                  ))
	        humann2.add_field('DMND_RAM',
			          UserInput('\tHow many GB of RAM does diamond (as part of Humann2) need per thread',
				            self.dmndRam,
				            type=int,
                                            fineControlOnly=True
                                  ))
	        humann2.add_field('THREADS',
			          UserInput('\tHow many threads would you like for HumanN2',
				            conf.get_global_field('THREADS'),
				            type=int,
                                            fineControlOnly=True
                                  ))
	        humann2.add_field('TIME',
			          UserInput('\tHow many hours does Humann2 need',
				            self.time,
				            type=int,
                                            fineControlOnly=True
                                  ))
	        humann2.add_field('RAM',
			          UserInput('\tHow many GB of RAM does Humann2 need per thread',
				            self.ram,
				            type=int,
                                            fineControlOnly=True
                                  ))


		
	@staticmethod
	def moduleName():
		return 'humann2'

		
modules.append(Humann2Module)

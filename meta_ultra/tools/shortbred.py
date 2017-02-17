import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.tools import *
from meta_ultra.conf_builder import *


class ShortBredSet( ToolSet):
	def __init__(self, **kwargs):
		super(ShortBredSet, self).__init__(**kwargs)
		self.ext = self.getParamOrAskUser('ext', default='.shortbred.tsv')
		self.time = self.getParamOrAskUser('time', default=1, type=int)
		self.ram = self.getParamOrAskUser('ram', default=4, type=int)

	def buildConf(self, confBuilder):
		shortbred = confBuilder.add_tool(self.toolSetName().upper())

		shortbred.add_field('EXT', self.ext)
		shortbred.add_field('EXC',
				    UserChoice('ShortBred Quantify',
					       self.excFiles,
					       new=lambda :self.askUserForExc('shortbred_quantify')
				    )),
		excFile = shortbred.get_field('EXC')
		shortbred.set_field('EXC', excFile.filepath)
		shortbred.set_field('VERSION', excFile.version)
		
		shortbred.add_field('DBS',
				    UserMultiChoice('ShortBred References',
						    self.refs,
						    new=lambda : self.askUserForRef('shortbred_quantify')
				    )),
		dbs = shortbred.get_field('DBS')
		dbPaths = []
		for db in dbs:
			dbPaths.append(db.filepath)
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
		
	@staticmethod
	def toolSetName():
		return 'shortbred'
		
toolsets.append(ShortBredSet)

import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *
from meta_ultra.conf_builder import *


class ShortBredModule( Module):
	def __init__(self, **kwargs):
		super(ShortBredModule, self).__init__(**kwargs)		
		self.ext = self.getParamOrDefault('ext', '.shortbred.tsv')
		self.time = self.getParamOrDefault('time', 1)
		self.ram = self.getParamOrDefault('ram', 4)

	def buildConf(self, confBuilder):
		shortbred = confBuilder.addModule(self.moduleName().upper())

		shortbred.add_field('EXT', self.ext)
		shortbred.add_field('EXC',
				    UserChoice('ShortBred Quantify',
					       self.tools,
					       new=lambda :self.askUserForTool('shortbred_quantify')
				    )),
		tool = shortbred.get_field('EXC')
		shortbred.set_field('EXC', tool.filepath)
		shortbred.set_field('VERSION', tool.version)
		
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
	def moduleName():
		return 'shortbred'

		
modules.append(ShortBredModule)
	# Utility Tools
	conf.add_tool('BOWTIE2')
	conf.add_tool('SAMTOOLS')
	conf.add_tool('DIAMOND')
	
	# shortbred
	shortbred = conf.add_tool('SHORTBRED')
	shortbred.add_field('EXT', '.shortbred.csv')
	shortbred.add_field('DBS',
			    MultiRefChoice('ShortBred DBs',
					   get_references(tool='shortbred'))),
	shortbred.add_field('THREADS',
			    UserInput('\tHow many threads would you like for shortbred',
				      conf.get_global_field('THREADS'),
				      type=int))
	shortbred.add_field('TIME',
			    UserInput('\tHow many hours does shortbred need',
				      1,
				      type=int))
	shortbred.add_field('RAM',
			    UserInput('\tHow many GB of RAM does shortbred need per thread',
				      5,
				      type=int))


	
	# metaphlan2
	metaphlan2 = conf.add_tool('METAPHLAN2')
	metaphlan2.add_field('EXT', '.metaphlan2.txt')
	metaphlan2.add_field('DB', RefChoice('MetaPhlAn2 DB',
					     get_references(tool='metaphlan2'))),
	metaphlan2.add_field('THREADS',
			     UserInput('\tHow many threads would you like for metaphlan2',
				       conf.get_global_field('THREADS'), type=int))
	metaphlan2.add_field('TIME',
			     UserInput('\tHow many hours does metaphlan2 need',
				       1,
				       type=int))
	metaphlan2.add_field('RAM',
			     UserInput('\tHow many GB of RAM does metaphlan2 need per thread',
				       5,
				       type=int))

	# panphlan
	panphlan = conf.add_tool('PANPHLAN')
	panphlan.add_field('EXT', '.panphlan.csv')
	panphlan.add_field('DB_DIR',
			   UserInput('\tWhere are the panphaln dbs located',
				     'panphlan_db'))
	panphlan.add_field('THREADS',
			   UserInput('\tHow many threads would you like for panphlan',
				     conf.get_global_field('THREADS'), type=int))
	panphlan.add_field('BT2_TIME',
			   UserInput('\tHow many hours does bowtie2 (as part of panphlan) need',
				     1,
				     type=int))
	panphlan.add_field('TIME',
			   UserInput('\tHow many hours does panphlan need',
				     1,
				     type=int))
	panphlan.add_field('BT2_RAM',
			   UserInput('\tHow many GB of RAM does bowtie2 (as part of panphlan) need per thread',
				     10,
				     type=int))
	panphlan.add_field('RAM',
			   UserInput('\tHow many GB of RAM does panphlan need per thread',
				     10,
				     type=int))


	# microbe census
	micCensus = conf.add_tool('MICROBE_CENSUS')
	micCensus.add_field('EXT', '.mic_census.txt')
	micCensus.add_field('THREADS',
			    UserInput('\tHow many threads would you like for MicrobeCensus',
				      conf.get_global_field('THREADS'),
				      type=int))
	micCensus.add_field('TIME',
			    UserInput('\tHow many hours does MicrobeCensus need',
				      1,
				      type=int))
	micCensus.add_field('RAM',
			    UserInput('\tHow many GB of RAM does MicrobeCensus need per thread',
				      10,
				      type=int))
	
	# kraken
	kraken = conf.add_tool('KRAKEN')
	kraken.add_field('RAW_EXT', '.raw_kraken.csv')
	kraken.add_field('MPA_EXT', '.mpa_kraken.csv')
	kraken.add_field('MPA_EXC',
			 UserInput('\tExceutable for kraken-mpa-report',
				   'kraken-mpa-report'))
	kraken.add_field('DB',
			 RefChoice('Kraken DB',
				   get_references(tool='kraken'))),
	kraken.add_field('THREADS',
			 UserInput('\tHow many threads would you like for kraken',
				   conf.get_global_field('THREADS'),
				   type=int))
	kraken.add_field('TIME',
			 UserInput('\tHow many hours does kraken need',
				   1,
				   type=int))
	kraken.add_field('MPA_TIME', '1')
	kraken.add_field('RAM',
			 UserInput('\tHow many GB of RAM does kraken need per thread',
				   10,
				   type=int))
	kraken.add_field('MPA_RAM', '1')

	# clark
	clark = conf.add_tool('CLARK')
	clark.add_field('EXT', '.clark')
	clark.add_field('THREADS', UserInput('\tHow many threads would you like for clark', conf.get_global_field('THREADS'), type=int))
	clark.add_field('TIME', UserInput('\tHow many hours does clark need', 1, type=int))
	clark.add_field('RAM', UserInput('\tHow many GB of RAM does clark need per thread', 10, type=int))


	# knead data
	kneadData = conf.add_tool('KNEADDATA')
	kneadData.add_field('DB',
			    RefChoice('KneadData DB',
				      get_references(tool='kneaddata'))),
	kneadData.add_field('THREADS',
			    UserInput('\tHow many threads would you like for KneadData',
				      conf.get_global_field('THREADS'),
				      type=int))
	kneadData.add_field('TIME',
			    UserInput('\tHow many hours does KneadData need',
				      1,
				      type=int))
	kneadData.add_field('RAM',
			    UserInput('\tHow many GB of RAM does KneadData need per thread',
				      10,
				      type=int))


	# humann2
	humann2 = conf.add_tool('HUMANN2')
	humann2.add_field('DB',
			  RefChoice('Humann2 DB',
				    get_references(tool='humann2'))),
	humann2.add_field('DMND_TIME',
			  UserInput('\tHow many hours does diamond (as a part of Humann2) need',
				    5,
				    type=int))
	humann2.add_field('DMND_THREADS',
			  UserInput('\tHow many threads would you like for diamond (as part of HumanN2)',
				    2*conf.get_global_field('THREADS'),
				    type=int))
	humann2.add_field('DMND_RAM',
			  UserInput('\tHow many GB of RAM does diamond (as part of Humann2) need per thread',
				    10,
				    type=int))
	humann2.add_field('THREADS',
			  UserInput('\tHow many threads would you like for HumanN2',
				    conf.get_global_field('THREADS'),
				    type=int))
	humann2.add_field('TIME',
			  UserInput('\tHow many hours does Humann2 need',
				    1,
				    type=int))
	humann2.add_field('RAM',
			  UserInput('\tHow many GB of RAM does Humann2 need per thread',
				    10,
				    type=int))
	
	# count classified reads
	countClass = conf.add_tool('COUNT_CLASSIFIED')

	# mash
	mash = conf.add_tool('MASH')



'''

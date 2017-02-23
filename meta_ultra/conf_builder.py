import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.user_input import *
import meta_ultra.modules as modules
import meta_ultra.sample_manager as SampleManager
import meta_ultra.database as mupdb
import sys
import json
import os
from tinydb import TinyDB, Query

################################################################################
#
# Data Classes 
#
################################################################################

def resolveVal(value, useDefaults, fineControl):

	if type(value) in [str, int, float, bool]:
		value = str(value)
		return value

	elif hasattr(value, 'to_dict'):
		value = resolveVal(value.to_dict(),
				   useDefaults,
				   fineControl
				   )

	elif type(value) not in [str, dict, list]:
		value = resolveVal(value.resolve(useDefaults=useDefaults, fineControl=fineControl),
				   useDefaults,
				   fineControl
				   )
	elif type(value) == dict:
		newVal = {}
		for k, v in value.items():
			newVal[k] = resolveVal(v, useDefaults, fineControl)
		value = newVal
	elif type(value) == list:
		newVal = []
		for el in value:
			newVal.append(resolveVal(el, useDefaults, fineControl))
		value = newVal	
	return value



class ConfBuilder:
	def __init__(self, useDefaults, fineControl):
		self.global_fields = {'TOOLS_TO_RUN':[]}
		self.tools = {}
		self.useDefaults = useDefaults
		self.fineControl = fineControl

	def add_global_field(self, key, value):
		self.global_fields[key] = resolveVal(value, self.useDefaults, self.fineControl)
	
	def addModule(self, tool_name):
		inp = ''
		while not self.useDefaults and 'y' not in inp and 'n' not in inp:
			inp = err_input('Include {} in this analysis? ([y]|n): '.format(tool_name))
			if not inp:
				inp = 'y'
		if 'y' in inp:
			self.tools[tool_name] = ToolBuilder(tool_name, self.useDefaults, self.fineControl)
			self.global_fields['TOOLS_TO_RUN'].append(tool_name)
			
		return self.tools[tool_name]

	def to_dict(self):
		out = self.global_fields
		for tool_name, builder in self.tools.items():
			out[tool_name] = builder.to_dict()
		return( out)

	def get_global_field(self,key):
		return self.global_fields[key]

	def set_global_field(self,key,val):
		# someday this might not do the same thing as add_global_field
		self.global_fields[key] = val

class ToolBuilder:
	def __init__(self,tool_name, useDefaults, fineControl):
		self.name = tool_name
		self.fields = {}
		self.useDefaults = useDefaults
		self.fineControl = fineControl
	
	def add_field(self,key,value):
		self.fields[key] = resolveVal(value, self.useDefaults, self.fineControl)

	def set_field(self,key,value):
		self.fields[key] = value

	def get_field(self,key):
		return self.fields[key]
	
	def to_dict(self):
		
		return self.fields

################################################################################
#
# Factory Functions
#
################################################################################
	
def add_samples_to_conf(confName,
			pairs=False,
			projectName=None,
			minReadLen=0,
			maxReadLen=250,
                        useDefaults=False,
                        fineControlOnly=False):
	
	finalConf = mupdb.Conf.get(confName).conf
	if not finalConf:
		msg = 'No conf with name {} found. Exiting.\n'.format(confName)
		sys.stdout.write(msg)
		sys.exit(1)

	newConf = ConfBuilder(useDefaults, fineControlOnly) 
	newConf.add_global_field('PAIRED_END', str(pairs))
	newConf.add_global_field('OUTPUT_DIR',
			      UserInput('Give the directory where output files '+
					'should go. All file paths will be '+
					'interpreted relative to the MUP_ROOT '+
					'enviroment variable',
                                        'results/'
                              ))
	outDir = newConf.get_global_field('OUTPUT_DIR')
	if not outDir.startswith(config.mup_root):
		if outDir[0] != '/':
			outDir = '/' + outDir
		outDir = config.mup_root + outDir
		newConf.set_global_field('OUTPUT_DIR',outDir)
                
	seq_data_recs = SampleManager.getSeqData(projectName=projectName,
						 paired=pairs,
						 lenMax=maxReadLen,
						 lenMin=minReadLen)
	if len(seq_data_recs) == 0:
		sys.stderr.write('No samples found. Exiting.\n')
		sys.exit(1)
		
	samples = {}
	for seq_data in seq_data_recs:
		samples[seq_data.sampleName] = {}
		samples[seq_data.sampleName]['PROJECT'] = seq_data.projectName
		samples[seq_data.sampleName]['DATA_NAME'] = seq_data.name
		samples[seq_data.sampleName]['1'] = seq_data.reads1
		if pairs:
			samples[seq_data.sampleName]['2'] = seq_data.reads2
	newConf.add_global_field('SAMPLES',samples)

	for k, v in newConf.to_dict().items():
		finalConf[k] = v
	return finalConf 

	
################################################################################
		
def buildNewConf(name, useDefaults=False, fineControl=False, modify=False):
	if mupdb.Conf.exists(name) and not modify:
		msg = 'Conf with name {} already exists. Exiting.\n'.format(name)
		sys.stderr.write(msg)
		sys.exit(1)

	confBldr = ConfBuilder(useDefaults, fineControl)

	# global opts	
	confBldr.add_global_field('NAME', name)
	confBldr.add_global_field('TMP_DIR',
			      UserInput('Please select a temporary directory',
					'/tmp'))
	confBldr.add_global_field('THREADS',
			      UserInput('How many threads would you like (you '+
					'will still be able to run multiple '+
					'jobs at once)',
					1,
					type=int))
	confBldr.add_global_field('EMAIL',
			      UserInput('Email to send progress reports to',
					None))
	confBldr.add_global_field('JOB_NAME_PREFIX',
			      UserInput('Prefix for job names',
					'MUP_'))

	# ToolSets register themselves by adding their class type
	# to the toolsets list. They then employ a visitor
	# pattern (ish) to add their own parameters to the conf.
	for moduleType in modules.modules:
		module = moduleType.build()
		module.buildConf(confBldr)

	
	conf_dict = confBldr.to_dict()

	confRecord = mupdb.Conf(**{'name': name, 'conf':conf_dict})
	return confRecord.save(modify=modify)
	
################################################################################


'''
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

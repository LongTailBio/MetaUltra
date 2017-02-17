import meta_ultra.config as config
from meta_ultra.ref_manager import get_references
from meta_ultra.tool_manager import get_tools
from meta_ultra.utils import *
from meta_ultra.tools import *

import meta_ultra.database as mupdb
import sys
import json
import os
from tinydb import TinyDB, Query

################################################################################
#
# User Input Classes
#
################################################################################

class Resolvable:
	def __init__(self):
		self.resolved = False
		self.resolved_val = None

	def resolve(self, use_defaults=True):
		if self.resolved:
			return self.resolved_val
		res = self._resolve( use_defaults=use_defaults)
		self.resolved_val = res
		self.resolved = True
		return res

class ToolChoice( Resolvable):
	def __init__(self, name, options):
		super(ToolChoice, self).__init__()
		self.name = name
		self.options = options

	def _resolve(self, use_defaults):
		if len(self.options) == 1:
			return self.options[0] # return the tool itself
		if len(self.options) == 0:
			sys.stderr.write('No entries for tool: {} found. You can register tools with the \'add_tool\' command\n'.format(self.name))
			sys.exit(1)
		if use_defaults:
			return self.options[0].path
		
		sys.stderr.write('\tPlease select an option for {}:\n'.format(self.name))
		for i, el in enumerate(self.options):
			sys.stderr.write('\t\t[{}] {} {}\n'.format(i, el.name, el.version))
		choice = err_input('\tPlease enter the index of your choice [0]: ')
		try:
			choice = int(choice)
		except ValueError:
			choice = 0
		
		return self.options[choice] # return the tool itself. 

	
class RefChoice( Resolvable):
	def __init__(self, name, options):
		super(RefChoice, self).__init__()
		self.name = name
		self.options = options

	def _resolve(self, use_defaults):
		if len(self.options) == 1:
			return self.options[0].path
		if len(self.options) == 0:
			sys.stderr.write('No references for {} found. You can register references with the \'add_reference\' command\n'.format(self.name))
			sys.exit(1)
		if use_defaults:
			return self.options[0].path
		
		sys.stderr.write('\tPlease select an option for {}:\n'.format(self.name))
		for i, el in enumerate(self.options):
			sys.stderr.write('\t\t[{}] {}\n'.format(i, el.name))
		choice = err_input('\tPlease enter the index of your choice [0]: ')
		try:
			choice = int(choice)
		except ValueError:
			choice = 0
		
		return self.options[choice].path

class MultiRefChoice( Resolvable):
	def __init__(self, name, options):
		super(MultiRefChoice, self).__init__()
		self.name = name
		self.options = options

	def _resolve(self, use_defaults):
		if len(self.options) == 1:
			return self.options[0].path
		if len(self.options) == 0:
			sys.stderr.write('No references for {} found. You can register references with the \'add_reference\' command\n'.format(self.name))
			sys.exit(1)
		if use_defaults:
			return self.options[0].path

		choices = []
		select_more_refs = True
		while select_more_refs:
			sys.stderr.write('\tPlease select an option for {}:\n'.format(self.name))
			for i, el in enumerate(self.options):
				sys.stderr.write('\t\t[{}] {}\n'.format(i, el.name))
			choice = err_input('\tPlease enter the index of your choice [0]: ')
			try:
				choice = int(choice)
			except ValueError:
				choice = 0
			choices.append(choice)
			
			more = err_input('Select another reference? (y/[n]): ')
			if 'y' not in more.lower():
				select_more_refs = False
				
		return { self.options[choice].name : self.options[choice].path for choice in choices}

	
class UserInput( Resolvable):
	def __init__(self, prompt, default, type=str):
		super(UserInput, self).__init__()
		self.prompt = prompt
		self.default = default
		self.type = type

	def _resolve(self, use_defaults=False):
		if use_defaults:
			return str(self.default)
		try_again = True
		while try_again:
			inp = err_input(self.prompt + ' [{}]: '.format(self.default))
			try_again = False
			if not inp: # use the default
				inp = self.default
				break
			try:
				self.type( inp) # we don't actually want to convert. We just want to make sure it's possible
			except ValueError:
				sys.stderr.write("Input must be of type '{}'".format(self.type))
				inp = None
				try_again = True
			
		
		return str(inp) # We want to treat defaults that aren't strings nicely

################################################################################
#
# Data Classes (Not as abstracted as it maybe should be)
#
################################################################################

class ConfBuilder:
	def __init__(self, use_defaults):
		self.global_fields = {'TOOLS_TO_RUN':[]}
		self.tools = {}
		self.use_defaults = use_defaults

	def add_global_field(self, key, value):
		if type(value) not in [str, dict, list]:
			value = value.resolve(use_defaults=self.use_defaults)
		self.global_fields[key] = value
	
	def add_tool(self, tool_name):
		inp = ''
		while not self.use_defaults and 'y' not in inp and 'n' not in inp:
			inp = err_input('Include {} in this analysis? ([y]|n): '.format(tool_name))
			if not inp:
				inp = 'y'
		if 'n' in inp:
			self.tools[tool_name] = ToolBuilder(tool_name, use_defaults=True)
		else:
			self.tools[tool_name] = ToolBuilder(tool_name, use_defaults=self.use_defaults)
			self.global_fields['TOOLS_TO_RUN'].append(tool_name)
			
		return self.tools[tool_name]

	def to_dict(self, use_defaults=False):
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
	def __init__(self,tool_name, use_defaults):
		self.name = tool_name
		self.fields = {}
		self.use_defaults = use_defaults

		toolChoice = ToolChoice(tool_name, get_tools(name=tool_name))
		tool = toolChoice.resolve(use_defaults=self.use_defaults)
		self.fields['EXC'] = tool.exc
		self.fields['VERSION'] = tool.version
	
	def add_field(self,key,value):
		if type(value) not in [str, dict, list]:
			value = value.resolve(use_defaults = self.use_defaults)
		self.fields[key] = value

	def to_dict(self, use_defaults=False):
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
			use_defaults=False):
	
	finalConf = mupdb.Conf.get(confName)['conf']
	if not finalConf:
		msg = 'No conf with name {} found. Exiting.\n'.format(confName)
		sys.stdout.write(msg)
		sys.exit(1)

	newConf = ConfBuilder(use_defaults) 
	newConf.add_global_field('PAIRED_END', str(pairs))
	newConf.add_global_field('OUTPUT_DIR',
			      UserInput('Give the directory where output files '+
					'should go. All file paths will be '+
					'interpreted relative to the MUP_ROOT '+
					'enviroment variable','results/'))
	outDir = conf.get_global_field('OUTPUT_DIR')
	if not outDir.startswith(config.mup_root):
		if outDir[0] != '/':
			outDir = '/' + outDir
		outDir = config.mup_root + outDir
		conf.set_global_field('OUTPUT_DIR',outDir)
	seq_data_recs = mupdb.get_seq_data(projectName=projectName,
					   paired=pairs,
					   lenMax=maxReadLen,
					   lenMin=minReadLen)
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
		assert k not in finalConf
		finalConf[k] = v
	return finalConf 

	
################################################################################
		
def build_and_save_new_conf(name, use_defaults=False, modify=False):
	if mupdb.Conf.exists(name) and not modify:
		msg = 'Conf with name {} already exists. Exiting.\n'.format(name)
		sys.stderr.write(msg)
		sys.exit(1)

	conf = ConfBuilder(use_defaults)

	# global opts	
	conf.add_global_field('NAME', name)
	conf.add_global_field('TMP_DIR',
			      UserInput('Please select a temporary directory',
					'/tmp'))
	conf.add_global_field('THREADS',
			      UserInput('How many threads would you like (you '+
					'will still be able to run multiple '+
					'jobs at once)',
					1,
					type=int))
	conf.add_global_field('EMAIL',
			      UserInput('Email to send progress reports to',
					None))
	conf.add_global_field('JOB_NAME_PREFIX',
			      UserInput('Prefix for job names',
					'MUP_'))

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

	'''
	# clark
	clark = conf.add_tool('CLARK')
	clark.add_field('EXT', '.clark')
	clark.add_field('THREADS', UserInput('\tHow many threads would you like for clark', conf.get_global_field('THREADS'), type=int))
	clark.add_field('TIME', UserInput('\tHow many hours does clark need', 1, type=int))
	clark.add_field('RAM', UserInput('\tHow many GB of RAM does clark need per thread', 10, type=int))
	'''

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
	
	conf_dict = conf.to_dict(use_defaults=use_defaults)

	confRecord = mupdb.Conf({'name': name, 'conf':conf_dict})
	confRecord.save(modify=modify)
	
################################################################################

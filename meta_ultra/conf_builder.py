from meta_ultra.utils import *
from meta_ultra.user_input import *
from meta_ultra.data_type import *
from meta_ultra.sample_type import *
import meta_ultra.modules as modules
import meta_ultra.api as api
import sys
import json
import os
import os.path

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

		try:	
			return self.tools[tool_name]
		except KeyError:
			return None

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
	
def addSamplesToConf(confName, dataRecs, useDefaults=False, fineControl=False):
	finalConf = api.getConf(confName).confDict
	if not finalConf:
		msg = 'No conf with name {} found. Exiting.\n'.format(confName)
		sys.stderr.write(msg)
		sys.exit(1)
		
	newConf = {}
	newConf['OUTPUT_DIR'] = UserInput('Give the directory where output files '+
					'should go.',
					'results/').resolve()
	outDir = newConf['OUTPUT_DIR']
		
	samples = {}
	for dataRec in dataRecs:
		if dataRec.sampleName not in samples:
			samples[dataRec.sampleName] = {}
			
		dataConf = {}
		samples[dataRec.sampleName][dataRec.name] = dataConf

		dataType = DataType.asDataType(dataRec.dataType)
		dataConf['PROJECT_NAME'] = dataRec.projectName
		dataConf['EXPERIMENT_NAME'] = dataRec.experimentName
		dataConf['DATA_NAME'] = dataRec.name
		dataConf['SAMPLE_NAME'] = dataRec.sampleName
		dataConf['DATA_TYPE'] = DataType.asString(dataRec.dataType)
		dataConf['SAMPLE_TYPE'] = SampleType.asString(dataRec.sampleType)

		if dataType == api.getDataTypes().WGS_DNA_SEQ_SINGLE_END:
			dataConf['1'] = dataRec.reads1

		elif dataType == api.getDataTypes().WGS_DNA_SEQ_PAIRED_END:
			dataConf['1'] = dataRec.reads1
			dataConf['2'] = dataRec.reads2


	
			
	newConf['SAMPLES'] = samples
	for k, v in newConf.items():
		finalConf[k] = v
	print(samples)
	return finalConf 

	
################################################################################
		
def buildNewConf(name, useDefaults=False, fineControl=False, modify=False):
	if api.getConf(name) and not modify:
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
	
	return api.saveConf(name, conf_dict)

################################################################################

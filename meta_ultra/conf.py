import meta_ultra.config as config
from meta_ultra.refs import get_references
from yaml import dump
import sys

class RefChoice:
	def __init__(self, name, options):
		self.name = name
		self.options = options

	def __str__(self):
		sys.stderr.write('Please select an option for {}:\n'.format(self.name))
		for i, el in enumerate(self.options):
			sys.stderr.write('\t[{}] {}\n'.format(i, el.name))
		choice = input('Please enter the index of your choice [0]: ')
		try:
			choice = int(choice)
		except ValueError:
			choice = 0
		
		return self.options[choice].path

class UserInput:
	def __init__(self, prompt, default):
		self.prompt = prompt
		self.default = default

	def __str__(self):
		inp = input(self.prompt + '[{}]: '.format(self.default))
		if not inp:
			inp = self.default
		return inp



	

class ConfBuilder:
	def __init__(self):
		self.global_fields = {}
		self.tools = {}

	def add_global_field(self, key, value):
		self.global_fields[key] = value
	
	def add_tool(self, tool_name):
		self.tools[tool_name] = ToolBuilder(tool_name)
		return self.tools[tool_name]

	def to_dict(self):
		out = resolve_dict(self.global_fields)
		for tool_name, builder in self.tools.items():
			inp = ''
			while 'y' not in inp and 'n' not in inp:
				inp = input('Include {} in this analysis? (y/n) [y]: '.format(tool_name))
				if not inp:
					inp = 'y'
			if 'n' in inp:
				continue
			
			out[tool_name] = builder.to_dict()
		return( out)

class ToolBuilder:
	def __init__(self,tool_name):
		self.name = tool_name
		self.fields = {}
	
	def add_field(self,key,value):
		self.fields[key] = value

	def to_dict(self):
		return( resolve_dict( self.fields))

			
def build_conf(samples, pairs=False):
	conf = ConfBuilder()

	if not pairs:
		samples = {sample:[sample] for sample in samples}
		conf.add_global_field('SAMPLES', samples)
	
	else:
		samplePairs = {}
		for sample in samples:
			sampleid = sample.split('_')[0]
			if sampleid not in samplePairs:
				samplePairs[sampleid] = []
			samplePairs[sampleid].append(sample)
		conf.add_global_field('SAMPLES', samplePairs)

	
	# global opts
	conf.add_global_field('TMP_DIR', UserInput('Please select a temporary directory', '/tmp'))


	# shortbred
	shortbred = conf.add_tool('SHORTBRED')
	shortbred.add_field('EXT', '.shortbred.csv')
	shortbred.add_field('EXC', 'shortbred_quantify.py')
	shortbred.add_field('DB', RefChoice('ShortBred DB',get_references(tool='shortbred'))),
	shortbred.add_field('THREADS',4)
	
	print( dump( conf.to_dict()))

def resolve_dict(el):
	if type(el) == str:
		return el
	elif type(el) == list:
		out = []
		for subel in el:
			out.append( resolve_dict(subel))
		return out
	elif type(el) == dict:
		out = {}
		for k, v in el.items():
			out[resolve_dict(k)] = resolve_dict(v)
		return out
	else:
		return str(el)
		
	


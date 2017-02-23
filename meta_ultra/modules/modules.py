import meta_ultra.config as config
from meta_ultra.user_input import *

import sys
import json
import os
from tinydb import Query, where

moduleTbl = config.db_module_table

def allModules(default=False):
	out = []
	for module in modules:
		out.append(module.build(useDefaults=default))
	return out

def getModule(name, default=False):
	rec = moduleTbl().insert(self.to_dict())
			return type(self).build()

	def askUserForTool(self,toolName, asDict=False):
		print(asDict)
		filepath = UserInput('Give the filepath for tool {} in module {}'.format(toolName, self.name),
				None).resolve()
		version = UserInput('Give the tool\'s version',default='unknown').resolve()
		tool = Tool(name=toolName, version=version,filepath=filepath)
		self.addTool(tool)
		if asDict:
			print('FOOBAR')
			tool =	tool.to_dict()
			print(tool)
			return tool
		return tool

	def buildAddTool(self, toolName, version, filepath, asDict=False):
		tool = Tool(name=toolName, version=version,filepath=filepath)
		self.addTool(tool)
		if asDict:
			return tool.to_dict()
		return tool

	
	def addTool(self, tool):
		self.tools.append(tool)
		return self.save(modify=True)

	def removeTool(self,i,confirm=True):
		tool = self.tools[i]
		remove = True
		if confirm:
			remove = BoolUserInput('Remove tool {} from {}?'.format(tool,self.name),
                                               default=True).resolve()
		if remove:
			sys.stderr.write('Removing tool {} from {}.\n'.format(tool, self.name))
			del self.tools[i]
			self.save(modify=True)
		else:
			sys.stderr.write('Not removing tool {} from {}.\n'.format(tool, self.name))

	def getToolsOfType(self, type):
		return [tool for tool in self.tools if tool.name.lower() == type.lower()]

	def askUserForRef(self, toolName, asDict=False):
		filepath = UserInput('Give a filepath for a reference-db for tool {} in module'.format(toolName, self.name),
				     None).resolve()
		refName = UserInput('Give the name for the reference',default=os.path.basename(filepath)).resolve()
		ref = Reference(name=refName, tool_name=toolName, filepath=filepath)
		self.addRef(ref)
		if asDict:
			return ref.to_dict()
		return ref

	def buildAddRef(self, refName, toolName, filepath, asDict=False):
		ref = Reference(name=refName, tool_name=toolName, filepath=filepath)
		self.addRef(ref)
		if asDict:
			return ref.to_dict()
		return ref
	
	def addRef(self, ref):
		self.refs.append(ref)
		return self.save(modify=True) 

	def removeRef(self,i,confirm=True):
		ref = self.refs[i]
		remove = True
		if confirm:
			remove = BoolUserInput('Remove reference {} from {}?'.format(ref,self.name), default=True).resolve()
		if remove:
			sys.stderr.write('Removing reference {} from {}.\n'.format(ref, self.name))
			del self.refs[i]
			self.save(modify=True)
		else:
			sys.stderr.write('Not removing reference {} from {}.\n'.format(ref, self.name))
	
	def getParamOrAskUser(self,key,default=None,type=str):
		try:
			return self.params[key]
		except KeyError:
			msg = ('No value found for parameter {} in module {}.\n'.format(key, self.name)+
			       'Please supply an appropriate parameter')
			inp = UserInput(msg, default, type=type)
			val = inp.resolve()
			self.addParam(key,val)
			return inp.resolve()

	def getParamOrDefault(self,key,default):
		try:
			return self.params[key]
		except KeyError:
			return default

		
	
	def addParam(self, key, value):
		self.params[key] = value
		return self.save(modify=True)

	def removeParam(self,key,confirm=True):
		param = self.params[key]
		remove = True
		if confirm:
			remove = BoolUserInput('Remove parameter {}={} from {}?'.format(key,val,self.name), default=True)
		if remove:
			del param
			self.save(modify=True,requireKeyOverlap=True)
			sys.stderr.write('Removing parameter {}={} from {}.\n'.format(key,val, self.name))
		else:
			sys.stderr.write('Not removing parameter {}={} from {}.\n'.format(key, val, self.name))

	def __str__(self):
		out = '{}\n'.format(self.name)
		out += '\tTools\n'
		for i, tool in enumerate(self.tools):
			out += '\t{}\t{}\n'.format(i,tool)
		out += 'References\n'
		for i, ref in enumerate(self.refs):
			out += '\t{}\t{}\n'.format(i,ref)
		out += 'Parameters\n'
		for k,v in self.params.items():
			out += '\t{}\t{}\n'.format(k,v)
		return out
	
	@classmethod
	def exists(ctype):
		modName = ctype.moduleName().lower()
		return None != moduleTbl().get(where('name') == modName) 
		
	@classmethod
	def record(ctype):
		modName = ctype.moduleName().lower()
		return moduleTbl().get(where('name') == modName)

	@classmethod
	def build(ctype,useDefaults=False):
		modName = ctype.moduleName().lower()
		rec = moduleTbl().get(where('name') == modName)
		if not rec:
			rec = {'name':modName}
		return ctype(**rec, use_defaults=useDefaults)

'''
A list of all the registerd modules

toolsets add themselves to the list on import
'''
modules = []

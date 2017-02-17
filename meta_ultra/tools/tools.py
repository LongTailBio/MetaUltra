import meta_ultra.config as config
from meta_ultra.user_input import *

import sys
import json
import os
from tinydb import TinyDB, Query, where

db = TinyDB(config.db_file)
toolTbl = db.table(config.db_tool_set_table)


class ToolSetExistsError(Exception):
	pass

class Reference:
	def __init__(self, **kwargs):
		self.name = kwargs['name']
		self.toolName = kwargs['tool_name']
		self.filepath = kwargs['filepath']

	def to_dict(self):
		out = {
			'name': self.name,
			'tool_name':self.toolName,
			'filepath': self.filepath
			}
		return out

	def __str__(self):
		return self.name

class ExecutableFile:
	def __init__(self, **kwargs):
		self.name = kwargs['name']
		self.version = kwargs['version']
		self.filepath = kwargs['filepath']

	def to_dict(self):
		out = {
			'name' : self.name,
			'version' : self.version,
			'filepath': self.filepath
			}
		return out

	def __str__(self):
		return '{}\t{}'.format(self.name, self.version)
	
class ToolSet:

	def __init__(self, **kwargs):
		self.name = kwargs['name']
		self.excFiles = []
		if 'executable_files' in kwargs:
			for rec in kwargs['executable_files']:
				excFile = ExecutableFile(**rec)
				self.excFiles.append(excFile)

		try:
			self.refs = [Reference(**rec) for rec in kwargs['references']]
		except KeyError:
			self.refs = []

		try:
			self.params = kwargs['params']
		except KeyError:
			self.params = {}

	def to_dict(self):
		out = {
			'name': self.name.lower(),
			'executable_files': [excFile.to_dict() for excFile in self.excFiles],
			'references': [ref.to_dict() for ref in self.refs],
			'params': self.params
			}
		return out


	def save(self,modify=False):
		if type(self).exists() and not modify:
			raise ToolSetExistsError()
		elif type(self).exists() and modify:
			rec = self.record()
			mydict = self.to_dict()
			for k,v in mydict.items():
				if k in rec and type(v) == dict and type(rec[k]) == dict:
					for subk, subv in v.items():
						rec[k][subk] = subv
				else:
					rec[k] = v
				toolTbl.update(rec, eids=[rec.eid])
			return type(self).build()
		else:
			print(self.to_dict())
			toolTbl.insert(self.to_dict())
			return type(self).build()

	def askUserForExc(self,excName, asDict=False):
		filepath = UserInput('Give the filepath for tool {} in toolset {}'.format(excName, self.name),
				None).resolve()
		version = UserInput('Give the tool\'s version',default='unknown').resolve()
		excFile = ExecutableFile(name=excName, version=version,filepath=filepath)
		self.addExc(excFile)
		if asDict:
			return excFile.to_dict()
		return excFile
		
	def addExc(self, excFile):
		self.excFiles.append(excFile)
		return self.save(modify=True)


	def askUserForRef(self, toolName, asDict=False):
		filepath = UserInput('Give a filepath for a reference-db for tool {} in toolset'.format(toolName, self.name),
				     None).resolve()
		refName = UserInput('Give the name for the reference',default=os.path.basename(filepath)).resolve()
		ref = Reference(name=refName, tool_name=toolName, filepath=filepath)
		self.addRef(ref)
		if asDict:
			return ref.to_dict()
		return ref

	def addRef(self, ref):
		self.refs.append(ref)
		return self.save(modify=True) 


	def getParamOrAskUser(self,key,default=None,type=str):
		try:
			return self.params[key]
		except KeyError:
			msg = ('No value found for parameter {} in toolset {}.\n'.format(key, self.name)+
			       'Please supply an appropriate parameter')
			inp = UserInput(msg, default, type=type)
			val = inp.resolve()
			self.addParam(key,val)
			return inp.resolve()

	
	def addParam(self, key, value):
		self.params[key] = value
		return self.save(modify=True)
		
	@classmethod
	def exists(ctype):
		setName = ctype.toolSetName().lower()
		return None != toolTbl.get(where('name') == setName) 
		
	@classmethod
	def record(ctype):
		setName = ctype.toolSetName().lower()
		return toolTbl.get(where('name') == setName)

	@classmethod
	def build(ctype):
		setName = ctype.toolSetName().lower()
		rec = toolTbl.get(where('name') == setName)
		if not rec:
			rec = {'name':setName}
		return ctype(**rec)

'''
A list of all the registerd toolsets

toolsets add themselves to the list on import
'''
toolsets = []

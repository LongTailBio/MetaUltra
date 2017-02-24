import meta_ultra.config as config
from meta_ultra.utils import *


import sys
import os

################################################################################
#
# User Input Classes. These classes are also used when building toolchains.
#
################################################################################

class Resolvable:
	def __init__(self):
		self.resolved = False
		self.resolved_val = None

	def resolve(self, useDefaults=False, fineControl=False):
		if self.resolved:
			return self.resolved_val

		res = self._resolve(useDefaults, fineControl)
		self.resolved_val = res
		self.resolved = True
		return res

class UserChoice(Resolvable):
	'''
	Let a user pick a choice from a set of options.

	On resolution this will return a single element.
	'''
	def __init__(self, name, options, new=None, fineControlOnly=False):
		super(UserChoice, self).__init__()
		self.name = name
		self.opts = options
		self.fineOnly=fineControlOnly
		self.new = new
		
	def _resolve(self, useDefaults, fineControl):
		if (len(self.opts) == 1 and not self.new) or useDefaults or (self.fineOnly and not fineControl):
			return self.opts[0]
		elif len(self.opts) == 0 and not self.new:
			sys.stderr.write('No options for {} found.\n'.format(self.name))
			sys.exit(1)
			
		sys.stderr.write('\tPlease select an option for {}:\n'.format(self.name))
		for i, opt in enumerate(self.opts):
			sys.stderr.write('\t\t[{}] {}\n'.format(i, opt))
		if self.new:
			sys.stderr.write('\t\t[{}] Pick new\n'.format(len(self.opts)))
		choice = err_input('\tPlease enter the index of your choice [0]: ')
		try:
			choice = int(choice)
		except ValueError:
			choice = 0

		if choice == len(self.opts):
			return self.new()

		sys.stderr.write('Chose: {}\n'.format(self.opts[choice]))
		return self.opts[choice] 

class UserMultiChoice( Resolvable):
	'''
	lets a user select may options from a list

	On resolution this will return a list of options
	'''
	def __init__(self, name, options, new=None, fineControlOnly=False):
		super(UserMultiChoice, self).__init__()
		self.name = name
		self.opts = options
		self.fineOnly=fineControlOnly
		self.new = new

	def _resolve(self, useDefaults, fineControl):
		if (len(self.opts) == 1 and not self.new) or useDefaults or (self.fineOnly and not fineControl):
			return [self.opts[0]]
		elif len(self.opts) == 0 and not self.new:
			sys.stderr.write('No options for {} found.\n'.format(self.name))
			sys.exit(1)

		choices = []
		select_more_refs = True
		while select_more_refs:
			sys.stderr.write('\tPlease select an option for {}:\n'.format(self.name))
			for i, opt in enumerate(self.opts):
				sys.stderr.write('\t\t[{}] {}\n'.format(i, opt))
			if self.new:
				sys.stderr.write('\t\t[{}] Pick new\n'.format( len(self.opts)))
			choice = err_input('\tPlease enter the index of your choice [0]: ')
			try:
				choice = int(choice)
			except ValueError:
				choice = 0
			if choice == len(self.opts):
				choices.append( self.new())
			else:
				choices.append(self.opts[choice])
			more = err_input('Select another reference? (y/[n]): ')
			if 'y' not in more.lower():
				select_more_refs = False

		sys.stderr.write('Chose: {}\n'.format(' '.join([str(choice) for choice in choices])))
		return choices
	
class UserInput( Resolvable):
	def __init__(self, prompt, default, type=str, fineControlOnly=False):
		super(UserInput, self).__init__()
		self.prompt = prompt
		self.default = default
		self.type = type
		self.fineOnly = fineControlOnly

	def _resolve(self, useDefaults, fineControl):
		if useDefaults or (self.fineOnly and not fineControl):
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

class UserInputNoDefault( Resolvable):
	def __init__(self, prompt, type=str, fineControlOnly=False):
		super(UserInputNoDefault, self).__init__()
		self.prompt = prompt
		self.type = type
		self.fineOnly = fineControlOnly

	def _resolve(self, useDefaults, fineControl):
		if useDefaults or (self.fineOnly and not fineControl):
			return str(self.default)
		try_again = True
		while try_again:
			inp = err_input(self.prompt + ': ')
			try_again = False
			if not inp: # use the default
				try_again=True
			else:
				try:
					self.type( inp) # we don't actually want to convert. We just want to make sure it's possible
				except ValueError:
					sys.stderr.write("Input must be of type '{}'".format(self.type))
					inp = None
					try_again = True
		
		return str(inp) # We want to treat defaults that aren't strings nicely

	

class BoolUserInput( Resolvable):
	def __init__(self, prompt, default, type=str, fineControlOnly=False):
		super(BoolUserInput, self).__init__()
		self.prompt = prompt
		self.default = default
		self.type = type
		self.fineOnly = fineControlOnly

	def _resolve(self, useDefaults, fineControl):
		if useDefaults or (self.fineOnly and not fineControl):
			return str(self.default)
		try_again = True

		while try_again:
			if self.default:
				prompt = self.prompt + ' ([y]/n): '
			else:
				prompt = self.prompt + ' (y/[n]): '
			inp = err_input(prompt)
			try_again = False
			if not inp: # use the default
				inp = self.default
				break
			
			if 'y' in inp.lower():
				return True
			elif 'n' in inp.lower():
				return False
			else:
				sys.stderr.write("Input must be yes/no".format(self.type))
				inp = None
				try_again = True
		

	

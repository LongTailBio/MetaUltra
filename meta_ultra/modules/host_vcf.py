import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *

class HostVCFModule( Module):
	def __init__(self, **kwargs):
		super(HostVCFModule, self).__init__(**kwargs)		
		self.sortTime = 2
		self.sortRam = 10
		self.threads = 10
		self.freeBayesTime = 20
		self.freeBayesRam = 4

		
	def buildConf(self, conf):
		hostVCF = conf.addModule('HOST_VCF')
		if not hostVCF:
			return
		
		hostVCF.add_field('EXC',
				 UserChoice('FreeBayes Parallel',
					    self.getToolsOfType('freebayes-parallel'),
					    new=lambda : self.askUserForTool('freebayes-parallel')
				 ))

		hostVCF.add_field('GENERATE_REGIONS',
				 UserChoice('Generate Regions',
					    self.getToolsOfType('fata_generate_regions'),
					    new=lambda : self.askUserForTool('fasta_generate_regions')
				 ))

		
		hostVCF.add_field('DB',
				 UserChoice('Host Genome',
					    self.refs,
					    new=lambda : self.askUserForRef('Host Genome')
				 ))
		
		hostVCF.add_field('THREADS',
				 UserInput('\tHow many threads does freebayes parallel need',
					   self.threads,
					   type=int,
					   fineControlOnly=True
				 ))
		
		hostVCF.add_field('SORT_TIME',
				 UserInput('\tHow many hours does samtools sort need',
					   self.sortTime,
					   type=int,
					   fineControlOnly=True
				 ))
		hostVCF.add_field('FREEBAYES_TIME',
				 UserInput('\tHow many hours does freebayes need',
					   self.freeBayesTime,
					   type=int,
					   fineControlOnly=True
				 ))

		hostVCF.add_field('SORT_RAM',
				 UserInput('How much RAM does samtoolsSort',
					   self.sortRam,
					   type=int,
					   fineControlOnly=True
				 ))
		
		hostVCF.add_field('FREEBAYES_RAM',
				 UserInput('How much RAM does freebayes need',
					   self.freeBayesRam,
					   type=int,
					   fineControlOnly=True
				 ))

		
	@staticmethod
	def moduleName():
		return 'host_vcf'


	
		
modules.append(HostVCFModule)

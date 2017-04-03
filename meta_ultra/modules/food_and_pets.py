import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *

class FoodAndPetsModule( Module):
	def __init__(self, **kwargs):
		super(FoodAndPetsModule, self).__init__(**kwargs)		
		self.time = self.getParamOrDefault('time', 10)
		self.ram = self.getParamOrDefault('ram', 4)

	def buildConf(self, conf):
		foodPets = conf.addModule('FOOD_PETS')
		if not foodPets:
			return
		
		foodPets.add_field('COUNT_SCRIPT',
				     UserChoice('Script to convert alignments to counts',
						self.getToolsOfType('count_script'),
						new=lambda :self.askUserForTool('count_script')
				     ))
		foodPets.add_field('FASTQ_TO_FASTA',
				     UserChoice('Convert fastq to fasta',
						self.getToolsOfType('fastq_to_fasta'),
						new=lambda :self.askUserForTool('fastq_to_fasta')
				     ))
		foodPets.add_field('DB',
				     UserChoice('Food and Pets DB',
						self.refs,
						new=lambda :self.askUserForRef('food_and_pets')
				     ))
		foodPets.add_field('THREADS',
				     UserInput('\tHow many threads would you like for food and pets',
					       conf.get_global_field('THREADS'),
					       type=int,
					       fineControlOnly=True
				     ))
		foodPets.add_field('TIME',
				     UserInput('\tHow many hours does food and pets need to run',
					       self.time,
					       type=int,
					       fineControlOnly=True
				     ))
		foodPets.add_field('RAM',
				     UserInput('\tHow many GB of RAM does food and pets blast need per thread',
					       self.ram,
					       type=int,
					       fineControlOnly=True
				     ))


	@staticmethod
	def moduleName():
		return 'food_and_pets'

		
modules.append(FoodAndPetsModule)

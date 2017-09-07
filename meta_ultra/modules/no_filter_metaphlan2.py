import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *

class NoHostFilterMetaphlan2Module( Module):
	def __init__(self, **kwargs):
		super(NoHostFilterMetaphlan2Module, self).__init__(**kwargs)		
		
	def buildConf(self, conf):
		metaphlan2 = conf.addModule('NO_HOST_FILTER_METAPHLAN2')
		if not metaphlan2:
			return
				
	@staticmethod
	def moduleName():
		return 'no_host_filter_metaphlan2'

		
modules.append(NoHostFilterMetaphlan2Module)

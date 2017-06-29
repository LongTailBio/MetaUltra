import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *

class NoHostFilterKrakenModule( Module):
	def __init__(self, **kwargs):
		super(NoHostFilterKrakenModule, self).__init__(**kwargs)		
		
	def buildConf(self, conf):
		kraken = conf.addModule('NO_HOST_FILTER_KRAKEN')
		if not kraken:
			return
		
	@staticmethod
	def moduleName():
		return 'no_host_filter_kraken'


	
		
modules.append(NoHostFilterKrakenModule)

import meta_ultra.config as config
from meta_ultra.utils import *
from meta_ultra.modules import *


class HMPSiteDistsModule( Module):
	def __init__(self, **kwargs):
		super(HMPSiteDistsModule, self).__init__(**kwargs)		

	def buildConf(self, conf):
		hmp = conf.addModule('HMP_SITE_DISTS')
		if not hmp:
			return
		
		hmp.add_field('EXC',
			       UserChoice('HMP Distance Finding Script',
					  self.getToolsOfType('hmp_dists'),
					  new=lambda :self.askUserForTool('hmp_dists')
			       ))
		
	@staticmethod
	def moduleName():
		return 'hmp_site_dists'

		
modules.append(HMPSiteDistsModule)
	

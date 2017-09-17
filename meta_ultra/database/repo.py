from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import sys

class MURepoNotFoundError( Exception):
    pass

class Repo:

    def __init__(self, repoPath, caching=True):

        self.repoPath = repoPath
        if caching:
            self.repo = TinyDB(self.repoPath, storage=CachingMiddleware(JSONStorage))
        else:
            self.repo = TinyDB(self.repoPath)
    def close(self):
        self.repo.close()

    def table(self, tableName):
        return self.repo.table( tableName)


    @staticmethod
    def getRepo(searchDir='.', caching=True):
        searchDir = os.path.abspath(searchDir)
        if config.mu_repo_dir in os.listdir(searchDir):
            repoPath = os.path.join(searchDir,mu_repo_path)
            return Repo(repoPath, caching=caching)
        else:
            # recurse up
            up = os.path.dirname(searchDir)
            if up == searchDir:
                raise MURepoNotFoundError()
            else:
                return getRepo(searchDir=up, caching=caching)
        

db_conf_table = lambda : get_config().table('conf_table')        
db_mu_config_remotes = lambda : get_config().table('mu_config_remotes')

db_module_table = lambda : get_repo().table('module_table')
db_sample_table = lambda : get_repo().table('sample_table')
db_project_table = lambda : get_repo().table('project_table')
db_data_table = lambda : get_repo().table('data_table')
db_experiment_table = lambda : get_repo().table('experiment_table')
db_result_table = lambda : get_repo().table('result_table')
db_project_result_table = lambda : get_repo().table('project_result_table')


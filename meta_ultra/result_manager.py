
from meta_ultra.database import *
from tinydb import where

def registerResult(toolchain, projectName, sampleName, dataName, confName, resultFiles, modify=False):
    name = '{}|{}|{}'.format(toolchain, confName, dataName)
    out = {
        'name': name,
        'project_name': projectName,
        'sample_name': sampleName,
        'data_name': dataName,
        'conf_name': confName,
        'result_files':resultFiles
    }
    result = Result(**out)
    result.save(modify=modify)
    return result


def getResults(projectName=None, sampleName=None):
    if sampleName:
        return Result.dbTbl().search(where('sample_name') == sampleName)
    elif projectName:
        return Result.dbTbl().search(where('project_name') == projectName)
    return Result.all()




def toNameList(l):
    if not l:
        return []
    names = []
    for el in l:
        if type(el) == str:
            names.append(el)
        else:
            names.append(el.name)
    return names

################################################################################
#
# Info Retrieval
#
################################################################################

def getProjects():
    pass

############################################################

def getExperiments():
    pass

############################################################

def getConfs():
    pass

###########################################################

def getSamples(projects=None):
    projNames = toNameList(projects)

###########################################################
    
def getData(dataType=None, samples=None, experiments=None, projects=None):
    sampleNames = toNameList(samples)
    expNames = toNameList(experiments)
    projNames = toNameList(projects)

def getSingleEndedSeqData(samples=None, experiments=None, projects=None):
    return getData(SingleEndedSeqData.dataType(),
                   samples=samples,
                   experiments=experiments,
                   projects=projects
                   )

def getPairedEndedSeqData(samples=None, experiments=None, projects=None):
    return getData(PairedEndedSeqData.dataType(),
                   samples=samples,
                   experiments=experiments,
                   projects=projects
                   )


################################################################################
#
# Info Storage
#
################################################################################

def saveProject(name, metadata):
    pass

###########################################################

def saveSample(name, project, metadata):
    pass

###########################################################

def saveExperiment(name, dataType, metadata):
    pass

def saveSingleEndedSeqRun(name, metadata):
    return saveExperiment(name, SingleEndedSeqData.dataType(), metadata)

def savePairedEndedSeqRun(name, metadata):
    return saveExperiment(name, PairedEndedSeqData.dataType(), metadata)

###########################################################

def saveSingleEndedSeqData(name,
                           readFilename,
                           aveReadLen,
                           sample,
                           experiment,
                           project):
    pass

def savePairedEndedSeqData(name,
                           read1Filename,
                           read2Filename,
                           aveReadLen,
                           sample,
                           experiment,
                           project,
                           aveGapLen=None):
    pass

###########################################################

def saveResult(name, resultFilenames, data, conf, sample, project):
    pass

###########################################################

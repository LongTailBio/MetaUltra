import config
from yaml import dump

def build_conf(samples,pairs=False):

    print( open(config.default_conf).read())
    if not pairs:
        samples = {sample:[sample] for sample in samples}
        samples = {'SAMPLES': samples}
    
    else:
        samplePairs = {}
        for sample in samples:
            sampleid = sample.split('_')[0]
            if sampleid not in samplePairs:
                samplePairs[sampleid] = []
            samplePairs[sampleid].append(sample)
        samples = {'SAMPLES':samplePairs}
    print( dump( samples))
    


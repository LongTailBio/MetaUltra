import meta_ultra.config as config
from yaml import dump



default_conf = {
'TMP_DIR' : '/tmp',
'READ_1_EXT' : '_1.fastq.gz',
'READ_2_EXT' : '_2.fastq.gz',

'TOOLS_TO_RUN' : ['SHORTBRED'],

'SHORTBRED_ALL' : 'all-samples.shortbred.csv',
'SHORTBRED_EXT' : '.shortbred.csv',
'SHORTBRED_DB' : None,
'SHORTBREAD_THREADS' : 4,

'SAMPLES' : None

}

def build_conf(samples,pairs=False):
    conf = default_conf
    if not pairs:
        samples = {sample:[sample] for sample in samples}
        conf['SAMPLES'] =  samples
    
    else:
        samplePairs = {}
        for sample in samples:
            sampleid = sample.split('_')[0]
            if sampleid not in samplePairs:
                samplePairs[sampleid] = []
            samplePairs[sampleid].append(sample)
        conf['SAMPLES'] = samplePairs
    
    print( dump( conf))
    


#!/usr/bin/env python

import sys
import subprocess as sp
import json




msg = '''
A simple script which uses minhash to find distances between a sample and hmp sites

Arguments are rudimentary and positional:

     <cmd> [hmp site minhash] [sample minhash]

Output is a JSON string to stdout and in the following form:

{
gut:    <dist>
skin:  <dist>
throat: <dist>
}
'''

if len(sys.argv) != 3:
    sys.stderr.write(msg)
    sys.exit(1)

def mean(l):
    return sum(l) / len(l)
    
hmp = sys.argv[1]
sample = sys.argv[2]

skin = []
gut = []
throat = []

for line in sp.getoutput('mash dist {} {}'.format(hmp,sample)).split('\n'): 
    target, query, dist, foo, bar = line.split()
    sim = 1-float(dist)
    if 'skin' in target:
        skin.append( sim)
    elif 'gut' in target:
        gut.append( sim)
    elif 'throat' in target:
        throat.append( sim) 

        
out={
    'gut' : mean(gut),
    'skin' : mean(skin),
    'throat' : mean(throat)
    }

sys.stdout.write(json.dumps(out))

#!/usr/bin/env python

import re, sys, itertools
from collections import defaultdict
from sys import argv

"""
Script to get summary of case/control status by sex from a .fam file
Inputs: 1) .fam file
Usage example:
"python fam_summary.py pathto/.fam"
"""

fam = argv[1] 

female = []
male = []
unk = []

with open(fam) as D:
    for i in D:
        i = i.strip().split(' ')
        if i[4] == '2': # i[4] = sex; 1 = male, 2 = female, other = missing
            female.append(i[5]) # i[5] = phenotype; control = 1, case = 2, other = missing
        elif i[4] == '1':
            male.append(i[5])
        else:
            unk.append(i[5])

f_ctrl = len(list(filter(lambda x: x=='1', female)))
f_case = len(list(filter(lambda x: x=='2', female)))
m_ctrl = len(list(filter(lambda x: x=='1', male)))
m_case = len(list(filter(lambda x: x=='2', male)))

print ''
print 'Females:', len(female)
print ' Cases:', f_case
print ' Controls:', f_ctrl
print ''     
print 'Males:', len(male)
print ' Cases:', m_case
print ' Controls:', m_ctrl
print ''
print 'Missing sex:', len(unk)


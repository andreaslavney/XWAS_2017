#!/usr/bin/env python

import re, sys, itertools
from collections import defaultdict
from sys import argv

"""
Script to recode case/control status in a .fam file using the phenotype file
Inputs: 1) .fam file; 2) phenotype data file; 3) output file name
Usage example:
"python recode_phenotype.py pathto/.fam pathto/.txt nonGAIN_SCZ_recode_phen"
then use plink to recode and generate new files:
"plink --noweb --bfile nonGAIN_Schizophrenia_consent_GRU --pheno nonGAIN_SCZ_recode_phen.txt --make-bed --out nonGAIN_recoded"
"""

fam, phen, out = argv[1], argv[2], argv[3]

fam_list = [] # Want to preserve position-based order and duplicates in original .fam file

# Make list of individual IDs in .fam file (phenotype values should all be zero)
with open(fam) as D:
    for i in D:
        i = i.strip().split(' ') # [0] = family ID; [1] = individual ID; [4] = sex (1=male, 2=female, 0=unk); [5] = phenotype (1=ctrl, 2=case, other=missing)
        if i[0]==i[1]:
            fam_list.append([i[0][3:], i[1][3:], i[5]]) # family ID (minus 'NG-'), phen
        else:
            print "family and individual ID are different:", i # all of these are cases in which there is a duplicate individual in the .fam file but only one entry for thet ID in the phenotype file
            fam_list.append([i[0][3:], i[1][3:], i[5]]) # family ID (minus 'NG-'), phen
            
print len(fam_list), 'individuals in .fam file'

phen_dict = defaultdict(list)
ind_count = 0

with open(phen) as D1:
    for j in D1:
        if re.match('#',j):
            continue
        ind_count +=1
        j = j.strip().split('\t')
        phen_dict[j[5]].append(j[6]) # key = SOURCE_SUBJID2, value = AFFECTION_STATUS (1=ctrl, 2=case)

print ind_count, 'individuals in phenotype file;', len(phen_dict), 'unique individuals in phenotype dictionary' # checking that all individual IDs are unique

out = open(out+'.txt','w')
seen_IDs = defaultdict(int)

for m in fam_list:
    
    fam_ID, ind_ID, old_phen = m[0], m[1], m[2]
    if old_phen!='0':
        print 'Non-zero phenotype in .fam file:', m
        raise KeyboardInterrupt
    new_phen = phen_dict[fam_ID]
    if len(new_phen)!=1: # check for cases where multiple rsIDs map to same Affy ID
        print 'Error - multiple phenotypes mapped to same individual ID:', m, new_phen
        raise KeyboardInterrupt
    new_phen = new_phen[0]
    seen_IDs[fam_ID]+=1
    print >> out, ' '.join(['NG-'+fam_ID, 'NG-'+ind_ID, new_phen]) # add prefix back to IDs

out.close()

print 'Duplicate IDs:'
for k,v in seen_IDs.iteritems():
    if v>1:
        print k
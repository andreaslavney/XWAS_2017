#!/usr/bin/env python

import re, sys
from collections import defaultdict
from sys import argv

"""
Script to pull SNP IDs from an array marker data file to use to recode SNPs in a .bim or .map file.
Inputs: 1) .bim file; 2) marker data file; 3) output file name
Usage example:
"python recode_IDs.py pathto/.bim pathto/.csv rsID_list"
then use plink to recode and generate new files:
"./plink --noweb --bfile pathto/mydata --update-map pathto/rsID_list.txt --update-name --make-bed --out newfile"
"""

bim, X_ref, out = argv[1], argv[2], argv[3]

bim_dict = [] # Want to preserve position-based SNP order in original .bim file

# Make list of SNP IDs and positions in .bim file 
with open(bim) as D:
    for i in D:
        i = i.strip().split('\t')
        bim_dict.append([i[1], i[0]+'_'+i[3]]) # ID, chr_pos
        
print len(bim_dict), 'SNPs in .bim file'


marker_dict = defaultdict(str)

# Make ditionary of rsIDs in imputation legend file keyed on SNP position
with open(X_ref) as D1:
    for j in D1:
        if re.match('rs',j): # only consider SNPs with an rsID
            j = split('\s')
            line = j[0].split(':')
            print line[0], '23_'+line[1]
            marker_dict['23_'+line[1]] = line[0] #k =chr_pos, v = rsID

print len(marker_dict), 'SNPs in marker file'


out = open(out+'.txt','w')

for k in bim_dict:
    old_ID, old_pos = k[0], k[1]
    new = marker_dict[old_ID]
    new_ID, new_pos = new[0], new[1]
    print k, new
    if old_pos == new_pos:
        print >> out, '\t'.join([old_ID, new_ID])
    else:
        print "discordant pos:", old_ID, old_pos, new # will happen for PAR SNPs (chr = 25)
        #print >> out, '\t'.join([old_ID, new_ID])
        #if re.match('25',old_pos):
            #print 'PAR SNP - position OK; ignore conflict'
            #print >> out, '\t'.join([old_ID, new_ID])

out.close()

print ''
print 'REMINDER: Check that new file has same # lines as .bim file (',len(bim_dict),')'

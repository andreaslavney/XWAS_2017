#!/usr/bin/env python

import re, sys, itertools
from collections import defaultdict
from sys import argv

"""
Script to pull SNP IDs from an array marker data file to use to recode SNPs in a .bim or .map file.
Inputs: 1) .bim file; 2) marker data file; 3) output file name; 4) file name for duplicate SNPs to remove
Usage example:
"python recode_IDs.py pathto/.bim pathto/.csv rsID_list remove"
then use plink to recode and generate new files:
"./plink --noweb --bfile pathto/mydata --update-map pathto/rsID_list.txt --update-name --make-bed --out newfile"
"""

bim, markers, out, remove = argv[1], argv[2], argv[3], argv[4]

bim_list = [] # Want to preserve position-based SNP order and duplicates in original .bim file

# Make list of SNP IDs and positions in .bim file 
with open(bim) as D:
    for i in D:
        i = i.strip().split('\t')
        bim_list.append([i[1], i[0]+'_'+i[3]]) # ID, chr_pos
        
print len(bim_list), 'SNPs in .bim file'


marker_dict = defaultdict(list)

# Make ditionary of rsIDs in array data file keyed on other SNP ID (e.g. Affy ID)
marker_count = 0
with open(markers) as D1:
    for j in D1:
        if re.match('#',j):
            continue
        else:
            marker_count +=1
            j = re.sub('"','',j)
            j = j.split(',')
            #print j
            if j[2]=='X':
                chr = '23'
            elif j[2]=='Y':
                chr = '24'
            elif j[2]=='MT':
                chr = '26'
            else:
                chr = j[2]
            
            # to check for cases where one Affy ID maps to multiple rsIDs, append
                
            if j[1]=='---': # If no rsID, just use Affy ID
                #print j[0], j[1], chr+'_'+j[3]
                marker_dict[j[0]].append([j[0], chr+'_'+j[3]]) #k = Affy ID, v =  [Affy ID, chr_pos]  
            else:
                marker_dict[j[0]].append([j[1], chr+'_'+j[3]]) #k = Affy ID, v =  [rsID, chr_pos] 
                #marker_dict[j[0]] = [j[2], chr+'_'+j[4]] #k = Affy ID, v =  [rsID, chr_pos]

print marker_count, 'entries in marker file;', len(marker_dict), 'unique SNPs in marker dictionary' # checking that all Affy IDs are unique


out = open(out+'.txt','w')
seen_rsIDs = defaultdict(int)

for m in bim_list:
    
    old_ID, old_pos = m[0], m[1] # Affy ID and position
    new = marker_dict[old_ID]
    if len(new)!=1: # check for cases where multiple rsIDs map to same Affy ID (not expected - inspect manually)
        print 'Error - multiple rsIDs mapped to same AffyID:', m, new
        raise KeyboardInterrupt
    
    new = new[0]
    new_ID, new_pos = new[0], new[1]
    seen_rsIDs[new_ID]+=1
    
    if old_pos == new_pos:
        print >> out, '\t'.join([old_ID, new_ID])
    else:
        if re.match('---',new_pos): # if no position listed in the marker file, still replace the SNP ID
            print >> out, '\t'.join([old_ID, new_ID])
        elif re.match('25',old_pos): # chr25 = mitochondrial genome; we don't care about it
            print 'PAR SNP - position OK; ignore conflict'
            print >> out, '\t'.join([old_ID, new_ID])
        else: # if positions truely disagree, we trust the one associated with the rsIDs more, so still replace the SNP iD
            #print "discordant pos:", old_ID, old_pos, new
            print >> out, '\t'.join([old_ID, new_ID])

out.close()

print ''
print 'REMINDER: Check that new file has same # lines as .bim file (',len(bim_list),')'
print ''

out2 = open(remove+'.txt','w')

print 'Duplicate rsIDs (writing to '+remove+'):'
for k,v in seen_rsIDs.iteritems():
    if v>1:
        #print k
        print >> out2, k+'\t'+str(v)
        
out2.close()
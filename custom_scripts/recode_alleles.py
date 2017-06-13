#!/usr/bin/env python

import re, sys
from collections import defaultdict
from sys import argv

"""
Script to pull alleles from an array marker data file to use to recode alleles in a .bim or .map file.
Inputs: 1) .bim file; 2) marker data file; 3) output file name
Usage example:
"python recode_alleles.py pathto/AJ_SZ_QCed_3096_06-27-12.bim pathto/HumanOmni1-Quad_v1-0_B.csv recode_list"
then use plink to recode:
"./plink --bfile pathto/mydata --update-alleles pathto/recodelist.txt --make-bed --out newfile"
"""

bim, alleles, out = argv[1], argv[2], argv[3]

bim_dict = [] # Want to preserve position-based SNP order in original .bim file

# Make list of alleles in .bim file keyed on SNP ID (e.g. in AJ SCZ data set, alleles are coded as A and B)
with open(bim) as D:
    for i in D:
        i = i.strip().split('\t')
        bim_dict.append([i[1], i[4], i[5]])

alleles_dict = defaultdict(list)
reg = re.compile("\[|\]")

# Make ditionary of alleles in array file keyed on SNP ID (e.g. alleles coded as [A/G], etc.)
# ***Note: order is not not always ref/alt allele
with open(alleles) as D1:
    for j in D1:
        j = j.split(',')
        nucs = reg.sub('',j[3])
        alleles_dict[j[1]] = nucs.split('/')
        
out = open(out+'.txt','w')

for k in bim_dict:
    ID = k[0]
    old1, old2 = k[1], k[2]
    new = alleles_dict[ID]
    new1, new2 = new[0], new[1]
    print >> out, '\t'.join([ID, old1, old2, new1, new2])

out.close()
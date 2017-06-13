#!/usr/bin/env python

import re, sys, itertools
from collections import defaultdict
from sys import argv

"""
Script to reformat gene list from BioMart for gene-based XWAS.
Inputs: 1) gene list text file (rows = chr, gene_start, gene_end, ENSG_ID, HGNC_symbol); 2) output file name
Usage example:
"python reformat_gene_list.py gene_list.txt final_gene_list.txt"
"""

gene_list, out_file = argv[1], argv[2]

out = open(out_file,'w')

with open(gene_list) as D:
    for i in D:
        i = i.strip().split('\t')
        if len(i)>4:
            name = i[3]+':'+i[-1]
        else:
            name = i[3]
        print >> out, '\t'.join(['23',i[1],i[2],name])

out.close()
        

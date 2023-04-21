# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 21:25:37 2021

@author: one
"""
import re

file_path = ("D:/BMR-DS/Project 1/Dataset/Pathways_SMPDB.txt")
file = open(file_path,'r')

writein_path = ("D:/BMR-DS/Project 1/Dataset/Pathway_other.txt")
writein = open(writein_path, 'a')

PE_path = ("D:/BMR-DS/Project 1/Dataset/Pathway_PE.txt")
PE = open(PE_path, 'a')

PC_path = ("D:/BMR-DS/Project 1/Dataset/Pathway_PC.txt")
PC = open(PC_path, 'a')

TG_path = ("D:/BMR-DS/Project 1/Dataset/Pathway_TG.txt")
TG = open(TG_path, 'a')

CL_path = ("D:/BMR-DS/Project 1/Dataset/Pathway_CL.txt")
CL = open(CL_path, 'a')

# First, the items are ordered in A-Z, manually.
first = 0
for items in file.readlines():
    item = items.split('\t')[1]
    if re.match('Cardiolipin Biosynthesis(.*)', item):
        if first == 0:
            writein.write(items)
            first = 1
        CL.write(items)
    elif re.match('De Novo Triacylglycerol Biosynthesis(.*)', item):
        if first == 1:
            writein.write(items)
            first = 0
        TG.write(items)
    elif re.match('Phosphatidylcholine Biosynthesis(.*)', item):
        if first == 0:
            writein.write(items)
            first = 1 
        PC.write(items)
    elif re.match('Phosphatidylethanolamine Biosynthesis(.*)', item):
        if first == 1:
            writein.write(items)
            first = 0
        PE.write(items)
    else:
        writein.write(items)


file.close()
writein.close()
PE.close()
PC.close()
CL.close()
TG.close()

'''
把句子分成单词进行寻找！！！
synthesis
biosynthesis
degradation
metabolism
pathway
resistance
disease
deficiency
action
'''

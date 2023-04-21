# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:19:54 2022

@author: one
"""

import json
import re

enzymes_path = ("D:/BMR-DS/Project 1/Dataset/Classification_without_hyphen.json")
with open(enzymes_path, 'r', encoding = 'utf-8') as enzymes:
    enzymesDict = json.load(enzymes)
enzymes.close()

ec_path = ("D:/BMR-DS/Project 1/Dataset/KEGG_EC_without_hyphen.json")
with open(ec_path, 'r', encoding = 'utf-8') as ec:
    ecList = json.load(ec)
ec.close()


EngList = ['alpha', 'beta', 'gamma', 'delta',
           'epsilon', 'zeta', 'eta', 'theta',
           'lota', 'kappa', 'lambda', 'mu',
           'nu', 'xi', 'omicron', 'pi', 'Rho',
           'sigma', 'tau', 'upsilon', 'phi',
           'chi', 'psi', 'omega']

for name in enzymesDict:
    if name != "ase":
        for item in enzymesDict[name]:
            for i in range(len(EngList)):
                if EngList[i] in item.split():
                    newItem = item.replace(EngList[i], chr(i+945))
                    enzymesDict[name].append(newItem)
                    ecList[newItem.lower()] = ecList[item.lower()]
                    print(newItem)
    else:
        for subname in enzymesDict[name]:
            if subname =='other' or subname == 'synthase' or subname == 'lyase' or subname == 'ligase':
                for item in enzymesDict[name][subname]:
                    for i in range(len(EngList)):
                        if EngList[i] in item.split():
                            newItem = item.replace(EngList[i], chr(i+945))
                            enzymesDict[name][subname].append(newItem)
                            ecList[newItem.lower()] = ecList[item.lower()]
                            print(newItem)
            else:
                for subsubname in enzymesDict[name][subname]:
                    for item in enzymesDict[name][subname][subsubname]:
                        for i in range(len(EngList)):
                            if EngList[i] in item.split():
                                newItem = item.replace(EngList[i], chr(i+945))
                                enzymesDict[name][subname][subsubname].append(newItem)
                                ecList[newItem.lower()] = ecList[item.lower()]
                                print(newItem)

classify = open('D:/BMR-DS/Project 1/Dataset/Classification_new.json', 'w')
json.dump(enzymesDict, classify, indent = 4)
classify.close()

ecnumber = open('D:/BMR-DS/Project 1/Dataset/KEGG_EC_new.json', 'w')
json.dump(ecList, ecnumber, indent = 4)
ecnumber.close()

    

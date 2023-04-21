# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 09:31:39 2021

@author: one
"""

import re
import json

s = '(asdf) (vb)df)'
pattern = re.compile(r'[(](.*?)[)]', re.I)
print(pattern.findall(s))


enzymes_path = ("D:/BMR-DS/Project 1/Dataset/Classification.json")
with open(enzymes_path, 'r', encoding = 'utf-8') as enzymes:
    enzymes_dict = json.load(enzymes)
w_path = ("D:/BMR-DS/Project 1/Dataset/After_word.txt")
w = open(w_path, 'a', encoding = 'utf-8')

num1, num2, num3, num4, nummore = 0, 0, 0, 0, 0
num = 0
num_not_ase = 0
dict_num = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, 'more': 0}
list_endword = []
for dic in enzymes_dict:
    if dic != 'ase':
        num_not_ase += len(enzymes_dict[dic])

for dic in enzymes_dict['ase']:
    if dic == 'other' or dic == 'synthase' or dic == 'lyase' or dic == 'ligase':
        for item in enzymes_dict['ase'][dic]:
            if re.search(r'[(](.*?)[)]$', item) and pattern.findall(item)[-1] not in list_endword:
                list_endword.append(pattern.findall(item)[-1])
                w.write(pattern.findall(item)[-1])
                w.write('\n')
            num += 1
            s = len(item.split())
            if s <= 5:
                dict_num[str(s)] = int(dict_num[str(s)]) + 1
            elif s > 5:
                dict_num['more'] += 1
    else:
         for d in enzymes_dict['ase'][dic]:
             for item in enzymes_dict['ase'][dic][d]:
                 if re.search(r'[(](.*?)[)]&', item):
                     list_endword.append(pattern.findall(item)[-1])
                     w.write(pattern.findall(item)[-1])
                     w.write('\n')
                 #list_endword.extend(pattern.findall(item))
                 num += 1
                 s = len(item.split())
                 if s<= 5:
                     dict_num[str(s)] += 1
                 elif s > 5:
                     dict_num['more'] += 1
                         
print(list_endword)
print('How many words does one item in KEGG list contain?')
print('Analyze the number of items with differnt number of words in it:\n')
print ('Number of words   Number of items')
print ('  in one item       in the list')
for d in dict_num:
    if d == 'more':
        print ('      ' + d + '                 ' + str(dict_num[d]))
    else:
        print ('       ' + d + '                   ' + str(dict_num[d]))
print('\n')
print("The total number of items in the list is " + str(num+num_not_ase))
print("The total number of items ending with 'ase' is " + str(num))
print("The probability of items ending with 'ase is " + str(num/(num+num_not_ase)))
print("The probability of items containing less than 5 words is " + str((num-dict_num['more']-dict_num['5'])/num))
print("The probability of items containing less than 6 words is " + str((num-dict_num['more'])/num))
enzymes.close()
w.close()


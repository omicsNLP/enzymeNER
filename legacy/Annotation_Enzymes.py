# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 10:35:15 2021

@author: one
"""
#import numpy as np
#import pandas as pd
import json
import re
import os
import time
#from fuzzywuzzy import fuzz


# cyclic lipopeptide synthases

'''
file_path = 'D:/BMR-DS/Project 1/Processing/PMC7093903_bioc.json'
with open(file_path, 'r', encoding = 'utf-8') as file: # windows 10 has the 'gbk' codec problem without encoding = 'utf-8'
    fulltext = json.load(file)                         # fulltext is a dict in python, after using json.load().
file.close()
'''


enzymes_path = ("D:/BMR-DS/Project 1/Dataset/Classification.json")
with open(enzymes_path, 'r', encoding = 'utf-8') as enzymes:
    enzymes_dict = json.load(enzymes)



def part_match(text, keyword, search_list): # search using "re"--before and after
    nonsense_list=['to', 'in', 'the', 'a', 'on', 'of', 'for', 'at', 'with','and','this','that','these','those','is','are']
    words = re.split('[ ,()/]', text.strip())
    index = 0
    for word in words:
        if word.lower().find(keyword)>=0:
            break
        index += 1
    start = text.lower().find(words[index])
    end = start + len(words[index])
    
    # RE match the word before the key word.
    pattern_before = re.compile('[(](.*)[)]')
    bracket = pattern_before.search(text, 0, start)
    temp = text[0:end].strip()
    if bracket != None:
        temp = text[0:bracket.start()]+text[bracket.end()+1:start]
    words_before = re.split(r'[ ,()/]', temp.strip()) 
    for word in words_before:
        if word == '':
            words_before.remove(word)
    index=len(words_before)-1
    for i in range(1, 4):
        if index - i >= 0:
            word = words_before[index-i].lower()
            flag = False
            for item in search_list:
                for part in re.split('[ ,/()-]', item.strip()):
                    if (word not in nonsense_list) and (not re.match('\d+', word)) and word == part.lower():
                        start = text.lower().rfind(word, 0, end)
                        flag = True
                        break 
                if flag == True:
                    break
            if flag == False:
                break
    # RE match the word after the key word.
    pattern_after = re.compile(r'complex|[A-Z]+(.*)|[(](.*?)[)]')#|[(](.*)[(](.*)[)][)]')#|[[](.*)[]]')
    pattern_after_after = re.compile(r'[(](.*?)[)]')
    after_word = pattern_after.match(text, end+1, len(text))
    if after_word != None:
        end = after_word.end()
        after_after_word = pattern_after_after.match(text, end+1, len(text))
        if after_after_word!= None:
            end = after_after_word.end()          
    # Return the entity
    entity = text[start:end]
    text = text[0 : start] + text[end+1: len(text)]
    return entity, text

def enzyme_ase(word):
    matchword = ''
    first_match = ''
    enzymes_list = []
    flag = 1 # If flag==0, search_list only has first_match.
    if re.match('(.*)synthase', word):
        first_match = 'synthase'
        flag = 0
    elif re.match('(.*)lyase', word):
        first_match = 'lyase'
        flag = 0
    elif re.match('(.*)ligase', word):
        first_match = 'ligase'
        flag = 0
    elif re.match('(.*)ease', word):
        first_match = 'ease'
        if re.match('(.*)permease', word):
            matchword = 'permease'
        elif re.match('(.*)protease', word):
            matchword = 'protease'
        else:
            matchword = 'other'
    elif re.match('(.*)lase', word):
        first_match = 'lase'
        if re.match('(.*)methylase', word):
            matchword = 'methylase'
        elif re.match('(.*)horylase', word):
            matchword = 'horylase'
        elif re.match('(.*)cyclase', word):
            matchword = 'cyclase'
        elif re.match('(.*)hydrolase', word):
            matchword = 'hydrolase'
        elif re.match('(.*)oxylase', word):
            matchword = 'oxylase'
        else:
            matchword = 'other'
    elif re.match('(.*)rase', word):
        first_match = 'rase'
        if re.match('(.*)transferase', word):
            matchword = 'transferase'
        elif re.match('(.*)saturase', word):
            matchword = 'saturase'
        else:
            matchword = 'other'
    elif re.match('(.*)tase', word):
        first_match = 'tase'
        if re.match('(.*)synthetase', word):
            matchword = 'synthetase'
        elif re.match('(.*)reductase(.*)', word):
            matchword = 'reductase'
        else:
            matchword = 'other'
    elif re.match('(.*)idase', word):
        first_match = 'idase'
        if re.match('(.*)oxidase', word):
            matchword = 'oxidase'
        elif re.match('(.*)peptidase', word):
            matchword = 'peptidase'
        else:
            matchword = 'other'
    elif re.match('(.*)nase', word):
        first_match = 'nase'
        if re.match('(.*)proteinase', word):
            matchword = 'proteinase'
        elif re.match('(.*)oxygenase', word):
            matchword = 'oxygenase'
        elif re.match('(.*)ogenase', word):
            matchword = 'ogenase'
        elif re.match('(.*)kinase', word):
            matchword = 'kinase'
        else:
            matchword = 'other'
    else:
        first_match = 'other'
        flag = 0
    if flag == 0:
        if first_match == 'other':
            flag_other = False
            for item in enzymes_dict['ase'][first_match]:
                for part in re.split('[ ,/()-]',item):
                    if part.lower() == word: #.strip(',').strip('/').strip('(').strip(')'):
                        enzymes_list = enzymes_dict['ase'][first_match]
                        flag_other = True
                        break
                if flag_other == True:
                    break
        else:
            enzymes_list = enzymes_dict['ase'][first_match]
        
    else:
        if matchword == 'other':
            flag_other = False
            for item in enzymes_dict['ase'][first_match][matchword]:
                for part in re.split('[ ,/()-]',item):
                    if part.lower() == word: #.strip(',').strip('/').strip('(').strip(')'):
                        enzymes_list = enzymes_dict['ase'][first_match][matchword]
                        flag_other = True
                        break
                if flag_other == True:
                    break
        else:
            enzymes_list = enzymes_dict['ase'][first_match][matchword]
    return enzymes_list


def search_ase(text, word):  
    search_list = enzyme_ase(word)
    flag = False # To mark if need to do part_match.
    entity = None
    if search_list:
        maxl = 0
        for item in search_list:
            if text.lower().find(item.lower())>0: # greedy
                if len(item) > maxl:
                   entity = item 
                   maxl = len(item)
        if entity != None:
            start = text.lower().find(entity.lower())
            entity = (text[start:start + len(entity)])
            text = text[0 : start] + text[(start + len(entity) + 1) : len(text)] # There is least one space between two words.
            flag = True
    else: # we assume that enzymes are all the types (ending with existed 'ase') which can be find inside the kegg, if it not existed in the kegg, we do not use RE to check the text.
        entity = None
        flag = True
    if flag == False:
        return part_match(text, word, search_list)
    return entity, text

def search_pattern(text, word, matchword):
    if matchword != 'ase':
        search_list = enzymes_dict[matchword]
        entity = None
        maxl = 0
        for item in search_list:
            if text.lower().find(item.lower())>0: # greedy
                if len(item) > maxl:
                   entity = item
                   maxl = len(item)
        if entity != None:
            start = text.lower().find(entity.lower())
            entity = text[start:start + len(entity)]
            text = text[0 : start] + text[(start + len(entity) + 1) : len(text)]
        return entity, text
    else:
        return search_ase(text, word)
        
def annotation_dictionary():
    dict={'text':'', 
                 'infons': {'identifier':'null',
                            'type':'enzyme',
                            'annotator':'m.wang21@imperial.ac.uk',
                            'updated_at':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                            },
                 'id':'',
                 'locations':{'length':'',
                              'offset':''
                              }
                }
    return dict

# if there is a request to give the past time of a verb?
notase_list = ['release','increase', 'database','base', 'disease','decrease', 'case']

# Patterns used to rematch.
pattern1 = re.compile(r'complex', re.I)
pattern2 = re.compile(r'enzyme', re.I)
pattern3 = re.compile(r'protein', re.I)
pattern4 = re.compile(r'transporter', re.I)
pattern5 = re.compile(r'Transferred')
pattern6 = re.compile(r'doxin', re.I)
pattern7 = re.compile(r'system', re.I)
pattern8 = re.compile(r'cytochrome', re.I)
pattern9 = re.compile(r'(.*)ase$|(.*)ases$')

id_num = 0
for filename in os.listdir('D:/BMR-DS/Project 1/Dataset/Microbiome - examples'):
    file_path = 'D:/BMR-DS/Project 1/Dataset/Microbiome - examples/' + filename
    with open(file_path, 'r', encoding = 'utf-8') as file: # windows 10 has the 'gbk' codec problem without encoding = 'utf-8'
        fulltext = json.load(file)           
    cont = 0 
    print(filename)
    for text in fulltext['documents'][0]['passages']:
        paragraph = text['text'].split('.')
        annotation = text['annotations']
        for sentence in paragraph:
            words = re.split('[ ,/()-]', sentence)
            matchword = ''
            for word in words:
                #while True:            
                if pattern1.search(word):
                    matchword = 'complex'
                elif pattern2.search(word):
                    matchword = 'enzyme'
                elif pattern3.search(word):
                    matchword = 'protein'
                elif pattern4.search(word):
                    matchword = 'transporter'
                elif pattern5.search(word):
                    matchword = 'Transferred'
                elif pattern6.search(word):
                    matchword = 'doxin'
                elif pattern7.search(word):
                    matchword = 'system'
                elif pattern8.search(word):
                    matchword = 'cytochrome'
                elif pattern9.search(word) and pattern9.search(word).group().rstrip('s').lower() not in notase_list:
                    matchword = 'ase'
                else:
                    matchword = 'other'
                    if word.lower() in enzymes_dict['other']:  # In this search_list, the words are all one-word.
                        id_num += 1
                        entity = word
                        annotation_dict = annotation_dictionary()
                        annotation_dict['text'] = entity
                        annotation_dict['id'] = str(id_num)
                        annotation_dict['locations']['length'] = len(entity)
                        annotation_dict['locations']['offset'] = int(fulltext['documents'][0]['passages'][cont]['offset']) + text['text'].find(entity)
                        annotation.append(annotation_dict)
                if matchword != 'other':
                    entity, content = search_pattern(sentence, word.rstrip('s').lower(), matchword) # Handle one sentence with multiple enzymes
                    if entity != None:
                        print(entity)
                        id_num += 1
                        annotation_dict = annotation_dictionary()
                        annotation_dict['text'] = entity
                        annotation_dict['id'] = str(id_num)
                        annotation_dict['locations']['length'] = len(entity)
                        annotation_dict['locations']['offset'] = int(fulltext['documents'][0]['passages'][cont]['offset']) + (text['text'].find(entity) + 1)

                        annotation.append(annotation_dict)
                        sentence = content
                        
        fulltext['documents'][0]['passages'][cont]['annotations'] = annotation
        cont += 1
    file.close()
    writein_path = "D:/BMR-DS/Project 1/Processing/" + filename.rstrip('.json') + '_' + 'annotation.json'
    writein = open(writein_path, 'w')
    json.dump(fulltext, writein, indent = 4)
    writein.close()

enzymes.close()
writein.close()
file.close()


# bovine neurosecretory granule protease cleaving pro-oxytocin/neurophysin



# Sentence should be divided into individual words to search the matching word.

# Problem
# hydroxyacid-oxoacid transhydrogenase; transhydrogenase, hydroxy acid-oxo acid
# There are more than one words in one sentence.--Try to search after one match until the end of sentence.

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 08:43:13 2021

@author: one
"""

import re
import os
import json
import time
from fuzzywuzzy import fuzz  
from fuzzywuzzy import process

start_time = time.time()
pathway_smpdb_path = ("D:/BMR-DS/Project 1/Dataset/Pathway_other.txt")
pathway_smpdb = open(pathway_smpdb_path, 'r')

pathway_kegg_path = ("D:/BMR-DS/Project 1/Dataset/Pathways_KEGG.txt")
pathway_kegg = open(pathway_kegg_path,'r')

file_path = ("D:/BMR-DS/Project 1/Processing/PMC3994512_bioc.json")
file = open(file_path,'r', encoding = 'utf-8')

pathway_lists = pathway_smpdb.readlines()
pathway_listk = pathway_kegg.readlines()
fulltext = json.load(file)  

pattern1 = re.compile(r'pathway', re.I)
pattern2 = re.compile(r'biosynthesis', re.I)
pattern3 = re.compile(r'degradation', re.I)
pattern4 = re.compile(r'action', re.I)
pattern5 = re.compile(r'metabolism', re.I)

space = ' '
nonsense_list=['an', 'II','/','-', 'or', 'all', 'no', '', 'at', 'other','to', 'in', 'the', 'a', 'on', 'of', 'for', 'at', 'with','and','this','that','these','those','is','are']

# search the before keyword.
def search_pathway(word):
    for item in pathway_lists:
        item = item.split('\t')[1]#item.lower().find(word.lower())>=0
        #print(item)
        '''
        if fuzz.partial_ratio(item.lower(), word.lower()) == 100 and word not in nonsense_list:
            return True
        '''
        for part in re.split('[ ]',item):
            # print(fuzz.partial_ratio(part, word))
            if part not in nonsense_list and not re.match ('[A-Z]', word) and not re.match('[0-9]', word) and (word.lower() == part.lower()):#>=0 or part.lower().find(word)>=0):#fuzz.partial_ratio(part.lower(), word.lower()) == 100:
                #print(part)
                return True
        
    return False
def add2list(entity):
    entity_list.append(entity)           
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


id_num = 0
cont = 0
for text in fulltext['documents'][0]['passages']:
    paragraph = text['text'].split('.')
    annotation = text['annotations']
    entity_list = []
    for sentence in paragraph:
        '''
        entity = None
        # Directly searching in the list.
        for item in pathway_lists:
            tmp = sentence
            find = sentence.lower().find(item[1])
            if find >= 0:
                end = find+len(item[1])
                entity = sentence[find : end]
                sentence = sentence[0:find] + sentence[end : len(sentence)]
            if entity == None or tmp == sentence:
                break
            else:
                print('In the list: ' + entity)
        '''
        # Use RE to supply the lost one.
        entity = None
        words = sentence.split()
        index = 0  
        while index < len(words):
            word = words[index].strip(',').strip('(').strip(')').strip('/')
            p4 = re.match(pattern4, word) # keyword == action
            if p4:
                if index + 1 < len(words):
                    p1 = pattern1.match(words[index+1].lower())
                    if p1:
                        if index - 2 > 0 and re.match('acid/acetate/(Antiarrhythmic)', words[index-1]) != None:
                            enitty = words[index-2] + space + words[index-1] + space + word + words[index+1]
                            add2list(entity)
                            id_num += 1
                            annotation_dict = annotation_dictionary()
                            annotation_dict['text'] = entity
                            annotation_dict['id'] = str(id_num)
                            annotation_dict['locations']['length'] = len(entity)
                            annotation_dict['locations']['offset'] = int(fulltext['documents'][0]['passages'][cont]['offset']) + (text['text'].find(entity) + 1)
                            annotation.append(annotation_dict)
                        elif index - 1 > 0:
                            entity = words[index-1] + space + word + space + words[index+1]
                            add2list(entity)
                            id_num += 1
                            annotation_dict = annotation_dictionary()
                            annotation_dict['text'] = entity
                            annotation_dict['id'] = str(id_num)
                            annotation_dict['locations']['length'] = len(entity)
                            annotation_dict['locations']['offset'] = int(fulltext['documents'][0]['passages'][cont]['offset']) + (text['text'].find(entity) + 1)
                            annotation.append(annotation_dict)
                        index += 1
                    else:
                        if words[index+1].lower() == 'action' and index + 2 < len(words) and pattern1.match(words[index+2].lower()):
                            entity = words[index-1] + space + word +space + words[index+1] + space + word[index+2]
                            add2list(entity)
                            index += 2
                            id_num += 1
                            annotation_dict = annotation_dictionary()
                            annotation_dict['text'] = entity
                            annotation_dict['id'] = str(id_num)
                            annotation_dict['locations']['length'] = len(entity)
                            annotation_dict['locations']['offset'] = int(fulltext['documents'][0]['passages'][cont]['offset']) + (text['text'].find(entity) + 1)
                            annotation.append(annotation_dict)
                        else:
                            if index - 2 >= 0 and re.match('H1-Antihistamine', word):
                                entity = words[index-2] + space + words[index+1] + space + word
                                add2list(entity)
                                index += 1
                                id_num += 1
                                annotation_dict = annotation_dictionary()
                                annotation_dict['text'] = entity
                                annotation_dict['id'] = str(id_num)
                                annotation_dict['locations']['length'] = len(entity)
                                annotation_dict['locations']['offset'] = int(fulltext['documents'][0]['passages'][cont]['offset']) + (text['text'].find(entity) + 1)
                                annotation.append(annotation_dict)
            elif re.match(pattern5, word):
                entity = word
                for i in range(1, 4):
                    if index - i > 0 and words[index-i] not in nonsense_list:
                        entity = words[index-i] + space + word
                    else:
                        break
                if index + 1 < len(words) and pattern1.match(words[index+1].lower()):
                    entity += (space + words[index+1])
                    index += 1                    
                if entity != word:
                    add2list(entity)
                    id_num += 1
                    annotation_dict = annotation_dictionary()
                    annotation_dict['text'] = entity
                    annotation_dict['id'] = str(id_num)
                    annotation_dict['locations']['length'] = len(entity)
                    annotation_dict['locations']['offset'] = int(fulltext['documents'][0]['passages'][cont]['offset']) + (text['text'].find(entity) + 1)
                    annotation.append(annotation_dict)
            elif re.match(pattern1, word) or re.match(pattern2, word) or re.match(pattern3, word) :
                entity = word
                for i in range(1, 4):
                    if index - i > 0 and words[index-i] not in nonsense_list and search_pathway(words[index-i]):
                        entity = words[index-i] + space + entity
                    else:
                        break
                if entity != word:
                    add2list(entity)
                    id_num += 1
                    annotation_dict = annotation_dictionary()
                    annotation_dict['text'] = entity
                    annotation_dict['id'] = str(id_num)
                    annotation_dict['locations']['length'] = len(entity)
                    annotation_dict['locations']['offset'] = int(fulltext['documents'][0]['passages'][cont]['offset']) + (text['text'].find(entity) + 1)
                    annotation.append(annotation_dict)
            index += 1
            '''
            elif re.match(pattern3, word):
                if index - 1 > 0 and words[index-1] not in nonsense_list and search_pathway(words[index-1]):
                    entity = words[index-1] + space + word
                    add2list(entity)
            elif re.match(pattern1, word):
                if index - 1 > 0 and words[index-1] not in nonsense_list and search_pathway(words[index-1]):
                    entity = words[index-1] + space + word
                    add2list(entity)
            '''
    cont += 1       
    if entity_list != []:
        print(entity_list)
                
pathway_smpdb.close()
pathway_kegg.close()
file.close()
end_time = time.time()
print(end_time - start_time)
'''
synthesis
biosynthesis
degradation
metabolism
'''

'''
... metabolism
... metabolism pathway

... action pathway
... action action pathway
... acid/acetate/(Antiarrhythmic) action pathway
... H1-Antihistamine action

'''  
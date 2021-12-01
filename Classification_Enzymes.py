# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 09:19:13 2021

@author: one
"""
import re
import json

file_path = ("D:/BMR-DS/Project 1/Dataset/KEGG_Enzymes.txt")
file = open(file_path,'r')

writein_path = ("D:/BMR-DS/Project 1/Dataset/Classification.json")
writein = open(writein_path, 'w')

#lost_path = ("")
#lost = open(lost_path,'a')

enzymes_dict = {'other':[], 
                'complex':[],
                'protein':[],
                'enzyme':[], 
                'transporter':[], 
                'Transferred':[], 
                'system':[],
                'cytochrome':[],
                'doxin':[],
                'ase':{'other':[],
                       'ease':{'other':[],
                               'permease':[],'protease':[],
                               },
                       'lase':{'other':[],
                               'methylase':[],'horylase':[],'cyclase':[],
                               'hydrolase':[],'oxylase':[]
                               },
                       'rase':{'other':[],  
                               'transferase':[],'saturase':[]
                               },
                       'tase':{'other':[],
                               'synthetase':[],'reductase':[]
                               },
                       'idase':{'other':[],
                                'oxidase' : [],'peptidase':[]
                                },
                       'nase':{'other':[],
                               'proteinase':[],'oxygenase':[],'ogenase':[],
                               'kinase':[], 
                               },
                       'synthase':[], 
                       'lyase':[],
                       'ligase':[]
                       }
                }

for i in file.readlines():
    if re.match('(.*)ase(.*)', i):
        if re.match('(.*)synthase(.*)', i):
            enzymes_dict['ase']['synthase'].append(i.strip('\n').strip())
        elif re.match('(.*)lyase(.*)', i):
            enzymes_dict['ase']['lyase'].append(i.strip('\n').strip())
        elif re.match('(.*)ligase(.*)', i):
            enzymes_dict['ase']['ligase'].append(i.strip('\n').strip())
        elif re.match('(.*)lase(.*)', i):
            if re.match('(.*)methylase(.*)', i):
                enzymes_dict['ase']['lase']['methylase'].append(i.strip('\n').strip())
            elif re.match('(.*)horylase(.*)', i):
                enzymes_dict['ase']['lase']['horylase'].append(i.strip('\n').strip())
            elif re.match('(.*)cyclase(.*)', i):
                enzymes_dict['ase']['lase']['cyclase'].append(i.strip('\n').strip())
            elif re.match('(.*)hydrolase(.*)', i):
                enzymes_dict['ase']['lase']['hydrolase'].append(i.strip('\n').strip())
            elif re.match('(.*)oxylase(.*)', i):
                enzymes_dict['ase']['lase']['oxylase'].append(i.strip('\n').strip())
            else:
                enzymes_dict['ase']['lase']['other'].append(i.strip('\n').strip())

        elif re.match('(.*)rase(.*)', i):
            if re.match('(.*)transferase(.*)', i):

                enzymes_dict['ase']['rase']['transferase'].append(i.strip('\n').strip())
            elif re.match('(.*)saturase(.*)', i):
                enzymes_dict['ase']['rase']['saturase'].append(i.strip('\n').strip())
            else:
                enzymes_dict['ase']['rase']['other'].append(i.strip('\n').strip())

        elif re.match('(.*)tase(.*)', i):

            if re.match('(.*)synthetase(.*)', i):
                enzymes_dict['ase']['tase']['synthetase'].append(i.strip('\n').strip())
            elif re.match('(.*)reductase(.*)', i):
                enzymes_dict['ase']['tase']['reductase'].append(i.strip('\n').strip())
            else:
                enzymes_dict['ase']['tase']['other'].append(i.strip('\n').strip())
        elif re.match('(.*)nase(.*)', i):
            if re.match('(.*)proteinase(.*)', i):
                enzymes_dict['ase']['nase']['proteinase'].append(i.strip('\n').strip())
            elif re.match('(.*)oxygenase(.*)', i):
                enzymes_dict['ase']['nase']['oxygenase'].append(i.strip('\n').strip())
            elif re.match('(.*)ogenase(.*)', i):
                enzymes_dict['ase']['nase']['ogenase'].append(i.strip('\n').strip())
            elif re.match('(.*)kinase(.*)', i):
                enzymes_dict['ase']['nase']['kinase'].append(i.strip('\n').strip())
            else:
                enzymes_dict['ase']['nase']['other'].append(i.strip('\n').strip())
        elif re.match('(.*)idase(.*)', i):
            if re.match('(.*)oxidase(.*)', i):
                enzymes_dict['ase']['idase']['oxidase'].append(i.strip('\n').strip())
            elif re.match('(.*)peptidase(.*)', i):
                enzymes_dict['ase']['idase']['peptidase'].append(i.strip('\n').strip())
            else:
                enzymes_dict['ase']['idase']['other'].append(i.strip('\n').strip())
        elif re.match('(.*)ease(.*)', i):
            if re.match('(.*)permease(.*)', i):
                enzymes_dict['ase']['ease']['permease'].append(i.strip('\n').strip())
            elif re.match('(.*)protease(.*)', i):
                enzymes_dict['ase']['ease']['protease'].append(i.strip('\n').strip())
            else:
                enzymes_dict['ase']['ease']['other'].append(i.strip('\n').strip())
        else:
            enzymes_dict['ase']['other'].append(i.strip('\n').strip())
    elif re.match('(.*)Transferred(.*)', i):
        enzymes_dict['Transferred'].append(i.strip('\n').strip())
    elif re.match('(.*)transporter(.*)', i):
        enzymes_dict['transporter'].append(i.strip('\n').strip())
    elif re.match('(.*)enzyme(.*)', i):
        enzymes_dict['enzyme'].append(i.strip('\n').strip())
    elif re.match('(.*)protein(.*)', i):
        enzymes_dict['protein'].append(i.strip('\n').strip())
    elif re.match('(.*)complex(.*)', i):
        enzymes_dict['complex'].append(i.strip('\n').strip())
    elif re.match('(.*)system(.*)', i):
        enzymes_dict['system'].append(i.strip('\n').strip())
    elif re.match('(.*)doxin(.*)', i):
        enzymes_dict['doxin'].append(i.strip('\n').strip())
    elif re.match('(.*)cytochrome(.*)', i):
        enzymes_dict['cytochrome'].append(i.strip('\n').strip())
    else:
        enzymes_dict['other'].append(i.strip('\n').strip())

     
json.dump(enzymes_dict, writein, indent=4)
'''
print ('The number of each stream:')
for i in enzymes_dict:
    if i != 'ase':
        print(str(i) + ':' + str(len(enzymes_dict[i])))
    else:
        for j in enzymes_dict[i]:
            if j =='ease' or j == 'lase' or j == 'rase' or j == 'tase' or j == 'idase' or j == 'nase':
                for x in enzymes_dict[i][j]:
                    print(str(x) + ':' + str(len(enzymes_dict[i][j][x])))
            else:
                print(str(j) + ':' + str(len(enzymes_dict[i][j])))
'''
file.close()
writein.close()

#lost.close()


# classification
# other--phospholipase, helicase, oximase, lactamase, duplicase, elongase
# Transferred to 
# ligase
# synthase--nitrososynthase

# lase--amylase, dealkylase,formylase,transformylase, sealase,  transcarbamoylase, thiolase, acylase, glycosylase, aldolase, ketolase, desmolase, deacetylase, sulfurylase 
# horylase--phosphorylase--transphosphorylase,pyrophosphorylase, diphosphorylase
# cyclase--oxidocyclase, oxydocyclase, 
# hydrolase--halidohydrolase,glycohydrolase, cyclohydrolase,
# oxylase--decarboxylase, carboxylase, hydroxylase, dehydroxylase
# methylase-hydroxymethylase, transhydroxymethylase, demethylase, transmethylase, dethiomethylase

# tase--transcriptase, aromatase, chelatase--cobaltochelatase, sulfatase,phosphodismutase, hydratase, dehydratase, pyrophosphatase, diphosphatase, homoaconitase, phosphatase, convertase, sphatase,  elastase, 
# synthetase--kinosynthetase

# nase--joinase, acetylenase, ketolactonase, sequenase,collagenase, endoxylanase, dechlorinase, amidinase, desulfinase, deaminase, eliminase, transoximinase,chlorinase, transaminase
# oxygenase--peroxygenase, lipoxygenase, dioxygenase, monooxygenase, 
# ogenase--dehydrogenase, transhydrogenase, dehalogenase, nitrogenase, drogenase, hydrogenase, halogenase
# kinase--sphokinase, deoxygalactonokinase, allokinase, arabinokinase, xylulokinase, fucokinase, acetokinase, carboxykinase, urokinase
# proteinase--metalloproteinase

# rase--luciferase, diaphorase, polymerase, cyclodehydrase, isomerase, epimerase, 
# transferase-- mycolyltransferase, amidinotransferase, amidotransferase,
# --phosphoribosyltransferase, ribosyltransferase, formyltransferase, methyltransferase,
# --dimethyltransferase, trimethyltransferase, hydroxyltransferase, hydroxymethyltransferase,
# --hydroxycinnamoyltransferase, formiminotransferase, benzoyltransferase, acetyltransferase, nucleotidyltransferase
# --acyltransferase, adenylyltransferase, guanylyltransferase, uridylyltransferase, 
# --carbamoyltransferase, cyclotransferase, cytidylyltransferase, phosphotransferase, 
# --oximinotransferase, aminotransferase, tuberculosinyltransferase, aminobutanoyltransferase, cistransferase, 
# --prenyltransferase, geranyltransferase,dimethylallyltransferase, carboxyethyltransferase
# --malonyltransferase, lauroyltransferase, aminobutyltransferase, decaprenylcistransferase, 
# --carboxyvinyltransferase, alkyltransferase, adenosyltransferase, aminopropyltransferase, enolpyruvyltransferase, 
# --pyruvatetransferase, formyltransferase, aminomethyltransferase
# --oligosaccharyltransferase, glucosyltransferase, glucuronosyltransferase, mannosyltransferase,
# --galactosyltransferase, acetylglucosaminyltransferase, glucosaminyltransferase, glutamyltransferase, glucanotransferase
# --succinyltransferase, myristoyltransferase, palmitoyltransferase

# lyase--amidolyase, hydrogenlyase, endolyase
# reductase--oxidoreductase, ferrireductase
# saturase--desaturase

# idase--mononucleotidase, isomaltotriosidase, amidase, mannosidase, glucosidase, ginsenosidase, glucosaminidase, fructosidase, ribonucleotidase
# oxidase--epoxidase(small)
# peptidase--carboxypeptidase, aminopeptidase, transpeptidase,

# ease--
# protease
# permease
# clease--ribonuclease, endonuclease, deoxyribonuclease, 









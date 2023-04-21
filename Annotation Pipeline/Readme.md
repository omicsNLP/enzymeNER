# Annotation Pipeline

## Pipeline

The oipeline is based on the strategy which classifies the enzyme-names through "root word" (as a tree-structure).

The searching process is running through the functions (```search_enzyme```, ```search_pattern```, ```search_ase```, ```part_match```, ```enzyme_ase_list```) defined in this script step-by-step, in which, the ```part_match``` is to detect the enzyme entity outside the given enzyme-list by using the "keyword".

We also provide some functions to process abbreviations (```abbre_search_enzyme```, ```abbre_enzyme_list```) which you can freely use.

## Enzyme Lists

Inside the "EnzymeLists" folder, There are three files:

```Classified_Enzyme_List.json```

```KEGG_EC_Enzymes.json```

```After_word.json```

All the files which are the given enzyme-relative lists and would be used during the processing have been provided.

## How to use

Run the code from the command line

```
python AnnotationEnzymes.py -i "path/to/input/data/from/Auto-CORPus" -o "path/to/output/folder/of/annotated/JSONfiles"
```

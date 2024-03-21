# enzymeNER
The enzymeNER contains four deep learning (DL) based models for named-entity recognition (NER) of enzyme which can be trained on the provided corpus for enzyme extraction from inputs. These DL models are based on [TABoLiSTM](https://github.com/omicsNLP/MetaboliteNER) (below) and fine-tuned models from Huggingface (see fine-tuned folder). A newly designed Annotation Pipeline is also included to automatically labelling enzyme entities in output files from [Auto-CORPus](https://github.com/omicsNLP/Auto-CORPus). bioRxiv paper [here](https://doi.org/10.1101/2023.06.23.546229).

[![DOI](https://zenodo.org/badge/418439604.svg)](https://zenodo.org/doi/10.5281/zenodo.10581586)
[![bioRxiv_DOI:10.1101/2023.06.23.546229](http://img.shields.io/badge/bioRxiv_DOI-10.1101/2023.06.23.546229-BE2536.svg)](https://doi.org/10.1101/2023.06.23.546229)

## Installation dependence
| Name | Version |
|------|---------|
|numpy|1.19.5|
|python|3.8.3|
|tensorflow|2.3.0|
|tokenizers|0.11.4|

## Train and evaluate the model
Run 'run.py' to start training or testing.

enzymeNER provides two DL-based models as word-embeddings (pretrained SciBERT and BioBERT, respectively).
As a first step you need to choose one word-embedding method through ```wdEmbed```.

```
python run.py --wdEmbed "SciBERT"
```

The bool variable ```isTrain``` controls the program to execute training or evaluation.
To train the model, ```isTrain``` should be True, and also ```train_set``` and ```train_annotset``` need to provided.

```
python run.py --wdEmbed "SciBERT" --isTrain True --train_set "./TrainingSet/TrainingSet.txt" --train_annotset "./TrainingSet/TrainingSetAnnot.txt"
```

To load a pretrained model, there are two required arguments, i.e.,  ```pretrain_model``` and ```test_json```.

```
python run.py --wdEmbed "SciBERT" --isTrain False --test_json "eNzymER_SciModel.json" --pretrain_model "./SciBertModels/epoch_9_SciModel_weights" 
```

To evaluate the model, aside from loading a model as above, a test set is a required input. For including ```test_set``` and ```test_annotset```, ```isTrain``` must be set to "False". The resulting output of the call are the metrics of the evaluation (Precision, Recall and F1-score) on the test set.

```
python run.py --wdEmbed "SciBERT" --isTrain False --test_json "eNzymER_SciModel.json" --pretrain_model "./SciBertModels/epoch_9_SciModel_weights" --test_set "./TestSet/test.txt" --test_annotset "./TestSet/testAnnotated.txt"
```

Alternatively, you can directly change the arguments from the defaults inside the ```run.py```, and then execute ```python run.py``` to run the code.

## Infer the model
To use the trained model to extract enzymes from input texts, you can use the 'process("input text")' function and the extracted entities will be given as output with their relative positions inside the input text.

Before that, you also need to set ```isTrain``` to ```False```, choose the method for word-embedding through ```wdEmbed```, and load the pretrained model.

```
import eNzymER_model
mdl = "scibert" # scibert or biobert
enz = eNzymER_model.eNzymER(mdl) # initialise
json_path = 'eNzymER_SciModel.json'
weight_path = './SciBertModels/epoch_9_SciModel_weights' # do not add a suffix here
enz.load(json_path,weight_path) # load model
```

Then use the process function to apply the model on sentences.

```
enz.process('The cysteine residue can be N-acetylated by cysteine conjugate N-acetyltransferases.')
```

Use the batchprocess function to apply the model on multiple split sentences. You can also vary the threshold (default = 0.5) to decide on inclusion of entities.

```
text_batch = ["In the glucose-alanine cycle pathway, glutamate dehydrogenase in muscle catalyzes the binding of α-ketoglutaric acid to ammonia to form glutamate, followed by glutamate catalyzed by alanine aminotransferase; pyruvic acid forms alpha-ketoglutarate and alanine [30].", "N1-methylinosine is found 3-adjacent to the anticodon at position 37 of eukaryotic tRNAs and is formed from inosine by a specific S-adenosylmethionine-dependent methylase.", "Pyruvate dehydrogenase (PDH), citrate synthase (CS), complete turnover of the TCA cycle, anaplerosis, and synthesis of glutamate and glutamine from glucose were evident in all eleven tumors."]
enz.batchprocess(text_batch, threshold=0.5)
```

Produces this output:

```
[[(38, 61, 'glutamate dehydrogenase'), (182, 206, 'alanine aminotransferase')],
 [(130, 170, 'S-adenosylmethionine-dependent methylase')],
 [(0, 22, 'Pyruvate dehydrogenase'), (30, 46, 'citrate synthase')]]
```

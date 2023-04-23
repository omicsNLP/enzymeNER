# enzymeNER
The enzymeNER contains two deep learning (DL) based models for named-entity recognition (NER) of enzyme which can be trained on the provided corpus for enzyme extraction from inputs. These DL models are based on [TABoLiSTM](https://github.com/omicsNLP/MetaboliteNER). A newly designed Annotation Pipeline is also included to automatically labelling enzyme entities in output files from [Auto-CORPus](https://github.com/omicsNLP/Auto-CORPus). 

## Installation dependence
| Name | Version |
|------|---------|
|numpy|1.19.5|
|python|3.8.3|
|tensorflow|2.3.0|
|tokenizers|0.11.4|

## Train and evaluate the model
Run 'run.py' to start training or testing.

enzymeNER provides two DL-based models as word-embeddings which are pretrained SciBERT and BioBERT respectively. So, first of all, you need to choose one word-embedding method through ```wdEmbed```.

e.g.

```
python run.py --wdEmbed "SciBERT"
```

The bool variable ```isTrain``` controls the program to execute training or evaluation.

To train the model, ```isTrain``` should be True, and also ```train_set``` and ```train_annotset``` are needed to provided.

e.g.

```
python run.py --wdEmbed "SciBERT" --isTrain True --train_set "./TrainingSet/TrainingSet.txt" --train_annotset "./TrainingSet/TrainingSetAnnot.txt"
```

To load a pretrained model, there are two arguments, i.e.,  ```pretrain_model``` and ```test_json```.

e.g.
```
python run.py --wdEmbed "SciBERT" --isTrain False --test_json "eNzymER_SciModel.json" --pretrain_model "./SciBertModels/epoch_9_SciModel_weights" 
```

To evaluate the model, besides loading model, the test set is needed. including ```test_set``` and ```test_annotset``` and ```isTrain``` must be "False". The metrics containing Precision, Recall and F1-score will output as the result.

e.g.

```
python run.py --wdEmbed "SciBERT" --isTrain False --test_json "eNzymER_SciModel.json" --pretrain_model "./SciBertModels/epoch_9_SciModel_weights" --test_set "./TestSet/test.txt"
--test_annotset "./TestSet/testAnnotated.txt"
```

OR you can directly change the arguments with the default inside the ```run.py```, and than just execute ``` python run.py``` to run the code.

## Infer the model
To use the well-trained model to extract the enzyme from input texts, use 'process("input text")' function and the extracted entities will be given back with their positions inside the input text.

```
@Joram will put some code in here as well, but Meiqi welcome to add yours.
```

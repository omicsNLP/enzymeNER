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

To load a pretrained model, there are two arguments, i.e.,  ```pretrain_model``` and ```test_json```.

e.g.
```
python run.py --isTrain False --test_json "eNzymER_SciModel.json" --pretrain_model "./SciBertModels/epoch_9_SciModel_weights" 
```

To evaluate the model, besides loading model, the test set is needed. including ```test_set``` and ```test_annotset```. The metrics containing Precision, Recall and F1-score will output as the result.

e.g.

```
python run.py --isTrain False --test_json "eNzymER_SciModel.json" --pretrain_model "./SciBertModels/epoch_9_SciModel_weights" --test_set "./TestSet/test.txt"
--test_annotset "./TestSet/testAnnotated.txt"
```


enzymeNER provides two DL-based model with two different word embedding algorithms which are pretrained SciBERT and BioBERT respectively. To use each model, only need to change the 'wdEmbed' to 'SciBERT' or 'BioBERT'.

## Infer the model
To use the well-trained model to extract the enzyme from input texts, use 'process("input text")' function and the extracted entities will be given back with their positions inside the input text.

```
@Joram will put some code in here as well, but Meiqi welcome to add yours.
```

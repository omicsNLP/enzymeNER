# enzymeNER
The enzymeNER contains two deep learning (DL) based models for named-entity recognition (NER) of enzyme which can be trained on the provided corpus for enzyme extraction from inputs. A newly designed Annotation Pipeline is also proposed for automatically labelling  enzyme-entities on training corpus. 

## Installation dependence
| Name | Version |
|------|---------|
|numpy|1.19.5|
|python|3.8.3|
|tensorflow|2.3.0|
|tokenizers|0.11.4|

## Train and evaluate the model
To Train the model, run 'run_train.py' to start training with the operation inside changing to 'train'. And when the operation is changed to 'test', this file will execute the evaluation process and The metrics including Precision, Recall and F1-score will output as the result.

```
@Meiqi, need to put some code in here please to make it easy for people.
```

enzymeNER provides two DL-based model with two different word embedding algorithms which are pretrained SciBERT and BioBERT respectively. To use each model, only need to change the 'wdEmbed' to 'SciBERT' or 'BioBERT'.

## Infer the model
To use the well-trained model to extract the enzyme from input texts, use 'process("input text")' function and the extracted entities will be given back with their positions inside the input text.

```
@Joram will put some code in here as well, but Meiqi welcome to add yours.
```

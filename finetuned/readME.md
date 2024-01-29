# enzymeNER
This folder contains code to fine tune models from Huggingface for NER tasks.
Example code is for a BioBERT model, other models are loaded and trained similarly.

from ner_experiment import create_dataloaders
from transformers import AutoTokenizer

biobert_name = 'dmis-lab/biobert-v1.1'
tokenizer_bb = AutoTokenizer.from_pretrained(biobert_name)
train_loader_bb, val_loader_bb, test_loader_bb = create_dataloaders(
    tokenizer=tokenizer_bb,
    train_folder='data/revision/train/', 
    val_folder='data/revision/val/', 
    test_folder='data/revision/test/',
    n_train=2500
)

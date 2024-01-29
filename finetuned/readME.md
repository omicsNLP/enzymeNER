# enzymeNER
This folder contains code to fine tune models from Huggingface for NER tasks.
Example code is for a SciBERT model, other models are loaded and trained similarly.

# Load required pre-requisites
```
from ner_experiment import create_dataloaders, train_via_trainer, test_via_trainer
from transformers import AutoTokenizer
```

# Choose model and input (change this to your own data, tsv format expected here)
```
hf_model = 'allenai/scibert_scivocab_uncased'
tokenizer_sb = AutoTokenizer.from_pretrained(hf_model)
train_loader_sb, val_loader_sb, test_loader_sb = create_dataloaders(
    tokenizer=tokenizer_sb,
    train_folder='data/train/', 
    val_folder='data/val/', 
    test_folder='data/test/',
    n_train=2500
)
```
# Start training with specific random state
```
i = 42
trainer_sb = train_via_trainer(
    train_loader_sb, val_loader_sb, 
    tokenizer_sb, model_name=hf_model,
    n_epochs=10, learning_rate=1e-4, verbose=False, seed=i
)
trainer_sb.print_val_mistakes = False
loss_val_epoch_sb, f1_sb, report_entities_sb, report_tokens_sb, trainer_sb = test_via_trainer(trainer_sb, test_loader_sb)   
```

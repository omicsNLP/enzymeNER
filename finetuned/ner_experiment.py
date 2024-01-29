from utils.tsv_processor import NerDataset
from utils.tsv_processor import read_data_from_folder, get_labels
from utils.opt import get_optimizer_with_weight_decay
from trainer import BertTrainer

import torch
from torch.optim import Adam
from torch.utils.data import DataLoader

from transformers import BertForTokenClassification
from transformers import get_linear_schedule_with_warmup

def create_dataloaders(
    tokenizer,
    train_folder='data/local_comp/train/', 
    val_folder='data/local_comp/val/', 
    test_folder='data/local_comp/test/',
    max_len_seq=128,
    batch_size=32,
    n_train=500,
    bs_only=False
):
    # limit sizes for prototyping (n_papers not n_sentences!)
    n_val = int(n_train * 0.5)
    n_test = n_val

    # new
    train_papers = read_data_from_folder(train_folder, bs_only=bs_only)
    val_papers = read_data_from_folder(val_folder, bs_only=False)
    tv_papers = {**train_papers, **val_papers}
    labels2ind, labels_count = get_labels(tv_papers)
    train_papers = dict(list(train_papers.items())[:n_train])
    train_set = NerDataset(
        corpus_sentences=train_papers, tokenizer=tokenizer, labels2ind=labels2ind, max_len_seq=max_len_seq
    )
    val_papers = dict(list(val_papers.items())[:n_val])
    val_set = NerDataset(
        corpus_sentences=val_papers, tokenizer=tokenizer, labels2ind=labels2ind, max_len_seq=max_len_seq
    )
    train_loader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(dataset=val_set, batch_size=batch_size, shuffle=False)

    # test loader
    test_papers = read_data_from_folder(test_folder, bs_only=False)
    test_papers = dict(list(test_papers.items())[:n_test])
    test_set = NerDataset(
        corpus_sentences=test_papers, tokenizer=tokenizer, labels2ind=labels2ind, max_len_seq=max_len_seq
    )
    test_loader = DataLoader(dataset=test_set, batch_size=batch_size, shuffle=False)

    print(f"Train: {train_set.get_num_papers()} papers, {train_set.get_num_sentences()} sentences.")
    print(f"Val: {val_set.get_num_papers()} papers, {val_set.get_num_sentences()} sentences.")
    print(f"Test: {test_set.get_num_papers()} papers, {test_set.get_num_sentences()} sentences.")
    
    return train_loader, val_loader, test_loader

def train_via_trainer(
    train_loader,
    val_loader,
    tokenizer,
    model_name,
    output_dir=None,
    n_epochs=2,
    learning_rate=1e-4,
    verbose=False,
    bs_only=False,
    f1_loss=False,
    seed=0,
):
    # training parameters
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"The device is {DEVICE}.")
    OPTIMIZER = Adam
    RATIO_WARMUP_STEPS = 0.1
    DROPOUT = 0.3
    ACCUMULATE_GRAD_EVERY = 4
    labels2ind = train_loader.dataset.label2ind

    if output_dir is None:
        short_name = "m"
        if model_name == 'allenai/scibert_scivocab_uncased':
            short_name = "scibert"
        elif model_name == 'dmis-lab/biobert-v1.1':
            short_name = "biobert"
        tsv_tag = 'Bs' if bs_only else 'ALL'
        output_dir = f'data/log/{short_name}_e{n_epochs}_classes{tsv_tag}'

    # set up tokenizer, model, and trainer
    nerbert = BertForTokenClassification.from_pretrained(
        model_name, hidden_dropout_prob=DROPOUT, attention_probs_dropout_prob=DROPOUT,
        num_labels=len(labels2ind), id2label={str(v): k for k, v in labels2ind.items()}
    )
    opt = get_optimizer_with_weight_decay(
        model=nerbert, optimizer=OPTIMIZER, learning_rate=learning_rate, weight_decay=0
    )
    train_steps = (len(train_loader) // ACCUMULATE_GRAD_EVERY) * n_epochs
    sched = get_linear_schedule_with_warmup(
        optimizer=opt, num_warmup_steps=train_steps*RATIO_WARMUP_STEPS, num_training_steps=train_steps
    )
    trainer = BertTrainer(
        model=nerbert, tokenizer=tokenizer, labels2ind=labels2ind,
        optimizer=opt, scheduler=sched, accumulate_grad_every=ACCUMULATE_GRAD_EVERY, 
        n_epochs=n_epochs, device=DEVICE, output_dir=output_dir, f1_loss=f1_loss,
        seed=seed
    )    
    if verbose:
        trainer.print_val_mistakes = True

    # run train-val loop
    trainer.train(dataloader_train=train_loader, dataloader_val=val_loader)
    return trainer

def test_via_trainer(trainer, test_loader):
    loss_val_epoch, f1, report_entities, report_tokens = trainer.evaluate(test_loader, verbose=True)
    return loss_val_epoch, f1, report_entities, report_tokens, trainer
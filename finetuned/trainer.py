import itertools
import os
from typing import List, Tuple, Union, Dict, Optional

from utils.custom_losses import SigmoidF1, MacroSoftF1

import numpy as np
import torch
from matplotlib import pyplot as plt
from seqeval.metrics import classification_report as seqeval_report
from seqeval.metrics import f1_score
from sklearn.metrics import classification_report as sklearn_report
from torch import nn
from torch.nn.modules.loss import CrossEntropyLoss
from torch.utils.data.dataloader import DataLoader
from transformers import PreTrainedModel, PreTrainedTokenizer
from transformers import set_seed

import torch.nn.functional as F


class BertTrainer:
    def __init__(self,
                 model: PreTrainedModel,
                 tokenizer: PreTrainedTokenizer,
                 optimizer: torch.optim.Optimizer,
                 n_epochs: int,
                 labels2ind: Dict[str, int],
                 scheduler: Optional[torch.optim.lr_scheduler.LambdaLR] = None,
                 device: str = 'cpu',
                 clipping: Optional[Union[int, float]] = None,
                 accumulate_grad_every: int = 1,
                 print_every: int = 10,
                 print_val_mistakes: bool = False,
                 output_dir: str = './',
                 f1_loss: bool = False,
                 seed: int = 0):

        """
        Complete training and evaluation loop in Pytorch specially designed for
        BERT-based models from transformers library. It allows to save the model
        from the epoch with the best F1-score and the tokenizer. The class
        optionally generates reports and figures with the obtained results that
        are automatically stored in disk.

        Args:
            model (`PreTrainedModel`): Pre-trained model from transformers library.
                For NER, usually loaded as `BertForTokenClassification.from_pretrained(...)`
            tokenizer (`PreTrainedTokenizer`): Pre-trained tokenizer from transformers library.
                Usually loaded as `AutoTokenizer.from_pretrained(...)`
            optimizer (`torch.optim.Optimizer`): Pytorch Optimizer
            n_epochs (`int`): Number of epochs to train.
            labels2ind (`dict`): maps `str` class labels into `int` indexes.
            scheduler (`torch.optim.lr_scheduler.LambdaLR`, `Optional`): Pytorch scheduler. It sets a
                different learning rate for each training step to update the network weights.
            device (`str`): Type of device where to train the network. It must be `cpu` or `cuda`.
            clipping (`int` or `float`, `Optional`): max norm to apply to the gradients. If None,
                no graddient clipping is applied.
            accumulate_grad_every (`int`): How often you want to accumulate the gradient. This is useful
                when there are limitations in the batch size due to memory issues. Let's say that in your
                GPU only fits a model with batch size of 8 and you want to try a batch size of 32. Then,
                you should set this parameter to 4 (8*4=32). Internally, a loop will be ran 4 times
                accumulating the gradient for each step. Later, the network parameters will be updated.
                So at the end, this is equivalent to train your network with a batch size of 32. The batch
                size is inferred from `dataloader_train` argument.
            print_every (`int`): How often you want to print loss. Measured in batches where a batch is
                considered batch_size * accumulate_grad_every.
            print_val_mistakes (`bool`): whether to print validation examples (sentences) where the model
                commits at least one mistake. It is printed after each epoch. The printed info is the word
                within each sentence, its predicted label and the real label. This is very useful to
                inspect the behaviour of your model.
            output_dir (`str`): Directory where file reports and images are saved.

        Methods:
            train(dataloader_train: DataLoader, dataloader_val: Optional[DataLoader] = None)
                Complete training and evaluation (optional) loop in Pytorch.
            evaluate(dataloader_val: DataLoader, epoch: int = 0, verbose: bool = False)
                Evaluation on test data.
        """

        set_seed(seed)
        self.tokenizer = tokenizer
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.n_epochs = n_epochs
        self.labels2ind = labels2ind
        self.inds2labels = {v: k for k, v in self.labels2ind.items()}
        self.device = device
        self.clipping = clipping
        self.accumulate_grad_every = accumulate_grad_every
        self.print_every = print_every
        self.print_val_mistakes = print_val_mistakes
        self.output_dir = output_dir
        self.f1_loss = f1_loss
        self.seed = seed

        os.makedirs(self.output_dir, exist_ok=True)

    def compute_loss():
        pass

    def _reformat_predictions(self,
                              y_true: List[List[int]],
                              y_pred: List[List[int]],
                              input_ids: List[List[str]]
                              ) -> Tuple[List[List[str]],
                                         List[List[str]],
                                         List[List[str]]]:
        """
        Takes batch of tokens, labels (class indexes) and predictions (class indexes)
        and get rid of unwanted tokens, that is, those that have as label the index
        to ignore (i.e. padding tokens).  It also converts the label and prediction
        indexes into their corresponding class name.
        Args:
            y_true (list of lists `int`): indexes of the real labels
            y_pred (list of lists `int`): indexes of the predicted classes
            input_ids (list of lists `str`) : tokens

        Returns:
            Tuple that contains the transformed input arguments

        """
        # Map indexes to labels and remove ignored indexes
        true_list = [[] for _ in range(len(y_true))]
        pred_list = [[] for _ in range(len(y_pred))]
        input_list = [[] for _ in range(len(input_ids))]

        for i in range(len(y_true)):
            for j in range(len(y_true[0])):
                if y_true[i][j] != CrossEntropyLoss().ignore_index:
                    true_list[i].append(self.inds2labels[y_true[i][j]])
                    pred_list[i].append(self.inds2labels[y_pred[i][j]])
                    input_list[i].append(input_ids[i][j])

        return true_list, pred_list, input_list

    def _print_missclassified_val_examples(self,
                                           y_true: List[List[str]],
                                           y_pred: List[List[str]],
                                           input_ids: List[List[str]]):
        """
        print validation examples (sentences) where the model commits at least
        one mistake. It is printed after each epoch. This is very useful to
        inspect the behaviour of your model.
        Args:
            y_true (list of lists `str`): real labels
            y_pred (list of lists `str`): predicted classes
            input_ids (list of lists `str`) : tokens

        Examples::
                TOKEN          LABEL          PRED
                immunostaining O              O
                showed         O              O
                the            O              O
                estrogen       B-cell_type    B-cell_type
                receptor       I-cell_type    I-cell_type
                cells          I-cell_type    O
                                  ·
                                  ·
                                  ·
                synovial       O              O
                tissues        O              O
                .              O              O

        """
        # Print some examples (where the model fails)
        for i in range(len(input_ids)):
            if y_true[i] != y_pred[i]:
                tokens = self.tokenizer.convert_ids_to_tokens(input_ids[i])
                max_len_token = max([len(t) for t in tokens] +
                                    [len(la) for la in self.labels2ind.keys()])

                print(f"\n{'TOKEN':<{max_len_token}}",
                      f"{'LABEL':<{max_len_token}}",
                      f"{'PRED':<{max_len_token}}")

                for token, label_true, label_pred in zip(tokens, y_true[i], y_pred[i]):
                    print(f"{token:<{max_len_token}}",
                          f"{label_true:<{max_len_token}}",
                          f"{label_pred:<{max_len_token}}")

    def _write_report_to_file(self,
                              report_entities: str,
                              report_tokens: str,
                              epoch: int,
                              tr_loss: float,
                              val_loss: float):
        """
        Writes and saves the following info into a file called `classification_report.txt`
        within the directory `output_dir` for the model from the best epoch:
            - Classification report at span/entity level (for validation dataset).
            - Classification report at word level (for validation dataset).
            - Epoch where the best model was found (best F1-score in validation dataset)
            - Training loss from the best epoch.
            - Validation loss from the best epoch.
        Args:
            report_entities (`str`): classification report at entity/span level.
            report_tokens (`str`): classification report at word level.
            epoch (`int`): epoch
            tr_loss (`float`): training loss
            val_loss (`float`): validation loss

        Returns:

        """
        with open(os.path.join(self.output_dir, 'classification_report.txt'), 'w') as f:
            f.write(report_entities)
            f.write(f'\n{report_tokens}')
            f.write(f"\nEpoch: {epoch} "
                    f"\n- Training Loss: {tr_loss}"
                    f"\n- Validation Loss: {val_loss}")

    def _save_model(self):
        if not isinstance(self.model, PreTrainedModel):
            raise ValueError("Trainer.model appears to not be a PreTrainedModel")
        self.model.save_pretrained(self.output_dir)
        self.tokenizer.save_pretrained(self.output_dir)

    def _estimate_gradients(self, batch: Dict[str, torch.Tensor]) -> float:
        # Send tensors to device
        batch = {k: v.to(self.device) for k, v in batch.items()}

        # estimate loss and gradient
        loss, logits = self.model(**batch, return_dict=False) # AV: add return_dict=False to get numbers
        
        if self.f1_loss:
            # loss_fn = SigmoidF1() # working but erribly
            loss_fn = MacroSoftF1()
            # have to use probabilities in loss
            probs = F.softmax(logits, dim=2)
            max_probs, predicted_classes = torch.max(probs, dim=2)
            loss = loss_fn(max_probs, batch['labels'])
        # print(loss)
        loss.backward()
        #print("past: backward")
        return loss.item()

    def _update_network_params(self):
        # Graddient clipping
        if self.clipping is not None:
            nn.utils.clip_grad_norm_(self.model.parameters(), self.clipping)

        # Udate parameters (accumulated gradient based on accumulated grad)
        self.optimizer.step()
        if self.scheduler is not None:
            self.scheduler.step()
        self.model.zero_grad()

    def _validation_step(self,
                         batch: Dict[str, torch.Tensor]
                         ) -> Tuple[float, np.ndarray]:
        # Send tensors to device
        batch = {k: v.to(self.device) for k, v in batch.items()}

        # Predict and estimate error
        with torch.no_grad():
            loss, pred = self.model(**batch, return_dict=False) # AV: don't return dict here

        return loss.item(), pred.detach().cpu().numpy()

    def evaluate(self,
                 dataloader_val: DataLoader,
                 epoch: int = 0,
                 verbose: bool = False) -> Tuple[float, float, str, str]:
        n_steps_val = len(dataloader_val)
        self.model.eval()

        val_loss_cum = .0
        y_pred = []
        y_true = []
        input_ids = []
        for step, batch in enumerate(dataloader_val):
            val_loss, pred = self._validation_step(batch)
            val_loss_cum += val_loss
            y_true.extend(batch['labels'].tolist())
            y_pred.extend(pred.argmax(axis=-1).tolist())
            input_ids.extend(batch['input_ids'].tolist())

        y_true, y_pred, input_ids = self._reformat_predictions(y_true, y_pred, input_ids)

        #print(y_true)
        for batch in y_pred:
            for i, pred_label in enumerate(batch):
                if pred_label == 'I':
                    batch[i] = 'B'
        for batch in y_true:
            for i, pred_label in enumerate(batch):
                if pred_label == 'I':
                    batch[i] = 'B'
        #print(y_true)
        # print(y_true, y_pred)

        # Performance Reports and loss
        report_entities = seqeval_report(y_true=y_true, y_pred=y_pred, digits=6)
        report_tokens = sklearn_report(y_true=list(itertools.chain(*y_true)),
                                       y_pred=list(itertools.chain(*y_pred)), digits=6)

        loss_val_epoch = val_loss_cum / n_steps_val

        if verbose:
            print(f"- Epoch: {epoch}/{self.n_epochs - 1} - Validation Loss: {loss_val_epoch}")
            print(report_entities)
            print(report_tokens)

        # Print some examples (where the model fails)
        if self.print_val_mistakes and verbose:
            self._print_missclassified_val_examples(y_true, y_pred, input_ids)

        # Save model and write report to txt file
        f1 = f1_score(y_true=y_true, y_pred=y_pred)

        return loss_val_epoch, f1, report_entities, report_tokens

    def train(self,
              dataloader_train: DataLoader,
              dataloader_val: Optional[DataLoader] = None
              ) -> Tuple[List[float], List[float]]:
        """
        Complete training and evaluation (optional) loop in Pytorch.
        Args:
            dataloader_train (`torch.utils.data.dataloader.DataLoader`): Pytorch dataloader.
            dataloader_val (`torch.utils.data.dataloader.DataLoader`, `Optional`):
                Pytorch dataloader. If `None` no validation will be performed.

        Returns:
            loss_tr_epochs (list of `float`): training loss for each epoch
            loss_val_epochs (list of `float`): validation loss for each epoch

        """
        loss_tr_epochs = []
        loss_val_epochs = []
        f1_best = .0
        lrs = []
        self.model.to(self.device)

        for epoch in range(self.n_epochs):
            tr_loss_mean = .0
            tr_loss_cum = .0
            step = -1

            # Training
            # -----------------------------
            self.model.train()
            self.model.zero_grad()
            for i, batch in enumerate(dataloader_train):
                # Estimate gradients and accumulate them
                tr_loss = self._estimate_gradients(batch)
                # print("past: estimate grad func")
                tr_loss_cum += tr_loss

                # Update params every acumulated steps
                if (i + 1) % self.accumulate_grad_every == 0:
                    self._update_network_params()
                    if self.scheduler is not None:
                        lrs.append(self.scheduler.get_last_lr()[0])
                    step += 1
                else:
                    continue
                # print("past: param update")

                if step % self.print_every == 0:
                    tr_loss_mean = tr_loss_cum/(i+1)
                    print(f"- Epoch: {epoch}/{self.n_epochs - 1}",
                          f"- Step: {step:3}/{(len(dataloader_train)// self.accumulate_grad_every) - 1}",
                          f"- Training Loss: {tr_loss_mean:.6f}")

            loss_tr_epochs.append(tr_loss_mean)
            print(f"- Epoch: {epoch}/{self.n_epochs - 1} - Training Loss: {tr_loss_mean}")

            # Plot training curve
            plt.plot(loss_tr_epochs)
            plt.xlabel('#Epochs')
            plt.ylabel('Error')
            plt.legend(['training'])

            # Validation
            # -----------------------------
            if dataloader_val is not None:
                val_loss, f1, report_ent, report_toks = self.evaluate(dataloader_val,
                                                                      epoch=epoch,
                                                                      verbose=True)
                loss_val_epochs.append(val_loss)

                if f1 > f1_best:
                    f1_best = f1
                    self._save_model()
                    self._write_report_to_file(report_ent, report_toks, epoch,
                                               tr_loss_mean, val_loss)

                # Plot val curve
                plt.plot(loss_val_epochs)
                plt.legend(['training', 'validation'])

            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'error_curves.jpg'))
            plt.close()

            # Plot learning rate curve
            plt.plot(lrs)
            plt.xlabel('#Batches')
            plt.ylabel('Learning rate')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, 'learning_rate.jpg'))
            plt.close()
        return loss_tr_epochs, loss_val_epochs


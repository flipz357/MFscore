import torch
import numpy as np

class ScorerFactory():

    def __init__(self):
        return None
	

    def get_scorer(self, modelstring):

        if "bert" in modelstring:
            scorer = BERTScorer(modelstring)
        elif "gpt2" in modelstring:
            scorer = GPT2Scorer(modelstring)
        else:
            scorer = None

        return scorer


class BertScorer():

    def __init__(self, modelstring="bert-base-cased"):
        from transformers import AutoTokenizer, BertForMaskedLM
        self.tok = AutoTokenizer.from_pretrained("bert-base-cased")
        self.bert = BertForMaskedLM.from_pretrained("bert-base-cased")

    def sent_score(self, sent):
        s = 0.0
        ss = sent.split()
        for i,w in enumerate(ss):
            curr = " ".join(ss[:i]) + " [MASK] " + " ".join(ss[i+1:])
            input_idx = tok.encode(f""+curr)
            maski = tok.convert_ids_to_tokens(input_idx).index("[MASK]")
            logits = bert(torch.tensor([input_idx]))[0]
            widx = tok.convert_tokens_to_ids([w])[0]
            probs = torch.nn.functional.softmax(logits, dim=1) 
            predictionscore = probs[0][maski][widx]
            sc = predictionscore.detach().numpy()
            s += sc
        if len(ss) == 0:
            return 0.0
        return s/len(ss)

class GPT2Scorer():
    
    def __init__(self, modelstring="gpt2", device="cpu", batch_size=1):
        from lm_scorer.models.auto import AutoLMScorer as LMScorer
        self.scorer = LMScorer.from_pretrained("gpt2", device=device, batch_size=batch_size)

    def sent_score(self, sent):
        ms = self.scorer.sentence_score(sent, reduce="mean")
        return ms



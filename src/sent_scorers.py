import torch
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ScorerFactory():

    def __init__(self):
        return None
	
    def get_scorer(self, scorer_uri):

        if "bert" in scorer_uri:
            scorer = BERTScorer(scorer_uri)
        elif "gpt2" in scorer_uri:
            scorer = GPT2Scorer(scorer_uri)
        else:
            scorer = None

        return scorer

class BERTScorer():

    def __init__(self, scorer_uri="bert-base-cased"):
        from transformers import AutoTokenizer, BertForMaskedLM
        self.tok = AutoTokenizer.from_pretrained(scorer_uri)
        self.bert = BertForMaskedLM.from_pretrained(scorer_uri)
    
    def score_sents(self, sents):
        scores = []
        for sent_num, sent in enumerate(sents):
            s = 0.0
            ss = sent.split()
            
            for i, w in enumerate(ss):
                curr = " ".join(ss[:i]) + " [MASK] " + " ".join(ss[i+1:])
                input_idx = self.tok.encode(f""+curr)
                maski = self.tok.convert_ids_to_tokens(input_idx).index("[MASK]")
                
                #shape (1, sent_len, n_vocab )
                logits = self.bert(torch.tensor([input_idx]))[0]
                probs = torch.nn.functional.softmax(logits, dim=1)     
                widx = self.tok.convert_tokens_to_ids([w])[0]
                predictionscore = probs[0][maski][widx]
                sc = predictionscore.detach().numpy()
                s += sc

            if len(ss) == 0:
                s =  0.0
            
            scores.append(s / len(ss))
            
            if (sent_num + 1) % 100 == 0:
                logger.info("{}/{} sentences scored".format(sent_num + 1
                    , len(sents)))
        return scores
        

class GPT2Scorer():
    
    def __init__(self, scorer_uri="gpt2", device="cpu", batch_size=16):
        from lm_scorer.models.auto import AutoLMScorer as LMScorer
        self.scorer = LMScorer.from_pretrained(scorer_uri, device=device
                , batch_size=batch_size)

    def score_sents(self, sents):
        scores = []
        for sent_num, sent in enumerate(sents):
            ms = self.scorer.sentence_score(sent, reduce="mean")
            scores.append(ms)
            if (sent_num + 1) % 100 == 0:
                logger.info("{}/{} sentences scored".format(sent_num + 1, len(sents)))
        return scores



import torch
import numpy as np

class CleanerFactory():

    def __init__(self):
        return None
	
    def get_cleaner(self, cleaner_uri="basic", acronyms=[]):
        if cleaner_uri == "basic":
            cleaner = BasicCleaner(acronyms)
        else:
            cleaner = None
        return cleaner


class BasicCleaner():

    def __init__(self, acronyms=[]):
        
        import spacy
        from sacremoses import MosesDetokenizer
        self.nlp = spacy.load("en_core_web_sm")
        self.md = MosesDetokenizer(lang="en")
        self.acronyms = acronyms
    
    def clean_sents(self, sents):

        sents = [s.lower() for s in sents]
        docs = [self.nlp(s) for s in sents]
        tokenss = [[tok.text for tok in doc] for doc in docs]

        detokenized_and_true_cased = []
        for i, toks in enumerate(tokenss):
            newtoks = []
            for j, tok in enumerate(toks):

                # sentence start -> capitalize
                if j == 0:
                    newtoks.append(tok.capitalize())

                # multi sentence sentence start -> capitalize
                elif newtoks[-1] == ".":
                    newtoks.append(tok.capitalize())

                # tok is PROPN ---> capitalize or uppercase if in acronyms
                elif docs[i][j].pos_ == "PROPN":
                    # nato ---> NATO
                    if tok.upper() in self.acronyms:
                        newtoks.append(tok.upper())
                    # barack obama ---> Barack Obama
                    else:
                        newtoks.append(tok.capitalize())

                #The chinese team ---> The Chinese team
                elif tok.capitalize() in self.acronyms:
                    newtoks.append(tok.capitalize())

                elif docs[i][j].pos_ == "PRON" and docs[i][j].text == "i":
                    newtoks.append(tok.capitalize())
                else:
                    newtoks.append(tok)
                
            detok = self.md.detokenize(newtoks)
            detokenized_and_true_cased.append(detok)
        return detokenized_and_true_cased




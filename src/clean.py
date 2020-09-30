import sys
import data_helpers as dh
import spacy
import argparse
from log_helper import get_logger

def build_arg_parser():

    parser = argparse.ArgumentParser(
            description='Clean sentences, and true-case')

    parser.add_argument('-generated_text_file_path'
            , type=str
            , help='file path to generated text')

    parser.add_argument('-source_amr_file_path'
            , type=str
            , default = None	
            , nargs='?'
            , help='file path to potential source file,\
                    it is only used to look up some\
                    acronyms like NATO for better\
                    true casing')

    parser.add_argument('-out_file_path'
            , type=str
            , nargs='?'
            , default = "tmp/out.clean"
            , help='output file path') 

    parser.add_argument('-out_file_path_ref_sents'
            , type=str
            , nargs='?'
            , default = "tmp/out.ref.clean"
            , help='output file path for AMR ref sentences') 
    

    parser.add_argument('-acronym_file_paths'
            , type=str
            , nargs='+'
            , default = None
            , help='file path to acronyms that are\
                    fully upper-cased') 
    
    parser.add_argument('-log_level'
            , type=int
            , nargs='?'
            , default=10
            , choices=list(range(0,60,10))
            , help='logging level (int), see\
                    https://docs.python.org/3/library/logging.html#logging-levels') 
    
    return parser



if __name__ == "__main__":

    args = build_arg_parser().parse_args()
    
    logger = get_logger('CleanerLogger', args.log_level)

    generated_text_raw_fp = args.generated_text_file_path
    source_file_amr_fp = args.source_amr_file_path
    acro_file_paths = args.acronym_file_paths
    acros = []
    for afp in acro_file_paths:
        acros += dh.readf(afp).split("\n")

    generated_text_raw = dh.readf(generated_text_raw_fp)

    lines = [l for l in generated_text_raw.split("\n")]
    
    lines = [l.replace(" @-@ "," - ").split() for l in lines]
    
    while not lines[-1]:
        lines = lines[:-1]
     
    if source_file_amr_fp:
        source_file_amr = dh.readf(source_file_amr_fp)

        amrref = source_file_amr
        amrreflines = [l for l in amrref.split("\n\n")]


        while not amrreflines[-1]:
            amrreflines = amrreflines[:-1]
        assert len(lines) == len(amrreflines)

    else:
        amrreflines = []

    true_cased = []

    nlp = spacy.load("en_core_web_sm")
    
    if source_file_amr_fp:
        sents = [l.split(" ::snt ")[1].split("\n")[0] for l in amrreflines]
        sents = [" ".join([t.text for t in nlp(s)]) for s in sents]
        sents = "\n".join(sents)
        with open(args.out_file_path_ref_sents, "w") as f:
            f.write(sents)
    
    
    
    nlp.tokenizer = nlp.tokenizer.tokens_from_list
    
    for i,toks in enumerate(lines):
        newtoks = []
        doc = nlp([t.lower() for t in toks])
        for j, tok in enumerate(toks):
            
            # sentence start -> capitalize
            if j == 0:
                newtoks.append(tok.capitalize())
            
            # multi sentence sentence start -> capitalize
            elif newtoks[-1] == ".":
                newtoks.append(tok.capitalize())

            # tok is PROPN ---> capitalize or uppercase if in acronyms
            elif doc[j].pos_ == "PROPN":
                # nato ---> NATO
                if tok.upper() in acros:
                    newtoks.append(tok.upper())
                # barack obama ---> Barack Obama
                else:
                    newtoks.append(tok.capitalize())                
            
            #The chinese team ---> The Chinese team
            elif tok.capitalize() in acros:
                newtoks.append(tok.capitalize())
            
            # if AMR ref and sentences are provided we search for some uppercase
            # or capitlized tokens that we may have missed with the above steps
            # e.g. "The us_NOUN wins the worldcup" (POS error for "us"), we look if in
            # the ref AMR there is (n / name :op1 "US") and then we can rectify this
            else:
                if "\""+tok.upper()+"\"" in dh.safe_get(amrreflines, i):
                    newtoks.append(tok.upper())
                elif "\""+tok.capitalize()+"\"" in dh.safe_get(amrreflines, i):
                    newtoks.append(tok.capitalize())
                else:
                    newtoks.append(tok)

        true_cased.append(newtoks)
        if (i + 1) % 100 == 0:
            logger.info("{}/{} sentences cleaned and true-cased".format(i+1, len(lines)))
    string = "\n".join([" ".join(toks) for toks in true_cased])
    if string.endswith("\n"):
        string = "\n".join(string.split("\n")[:-1])
    with open(args.out_file_path, "w") as f:
        f.write(string)
    logger.info("finished... result written to {}".format(args.out_file_path))




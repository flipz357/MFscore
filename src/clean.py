import sys
import data_helpers as dh
import spacy
import argparse
from log_helper import get_logger
from sent_cleaners import CleanerFactory

def build_arg_parser():

    parser = argparse.ArgumentParser(
            description='Clean sentences, and true-case')

    parser.add_argument('-input_file_path'
            , type=str
            , help='file path to text')
    
    parser.add_argument('-input_file_type'
            , type=str
            , required=True
            , choices=["amr-bank", "sent-per-line"]
            , help='input file either AMR sembank (\"amr-bank\") \
                    or sent per line (\"sent-per-line\")')

    parser.add_argument('-out_file_path'
            , type=str
            , nargs='?'
            , default = "tmp/out.clean"
            , help='output file path') 
    
    parser.add_argument('-cleaner_uri'
            , type=str
            , nargs='?'
            , default = "basic"
            , help='preprocessing type') 
    
    parser.add_argument('-acronym_file_paths'
            , type=str
            , nargs='+'
            , default = None
            , help='file pathes to acronyms that are\
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
    
    logger = get_logger('CleanLogger', args.log_level)

    input_text_raw_fp = args.input_file_path
    
    if args.input_file_type == "amr-bank":
        amrref = dh.readf(args.input_file_path)
        amrreflines = [l for l in amrref.split("\n\n")]
        sents = [l.split(" ::snt ")[1].split("\n")[0] for l in amrreflines]
    else:
        sents = dh.readf(args.input_file_path).split("\n")
    
    capitalization_help = set()
    for fi in args.acronym_file_paths:
        words = set(dh.readf(fi).split("\n"))
        capitalization_help.update(words)

    cleaner = CleanerFactory().get_cleaner(cleaner_uri="basic"
            , acronyms=capitalization_help)
    cleaned = cleaner.clean_sents(sents)

    #remove possible empty trailing lines
    while not cleaned[-1]:
        cleaned = cleaned[:-1]
    string = "\n".join(cleaned)
    
    with open(args.out_file_path, "w") as f:
        f.write(string)
    
    logger.info("finished... result written to {}".format(args.out_file_path))




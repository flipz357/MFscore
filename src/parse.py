import amrlib
from data_helpers import readf
import sys
import argparse
from log_helper import get_logger

def build_arg_parser():

    parser = argparse.ArgumentParser(
            description='AMR parsing')

    parser.add_argument('-text_file_path'
            , type=str
            , help='file path to text')
    
    parser.add_argument('-out_file_path'
            , type=str
            , default="tmp/out.stog_parsed"
            , help='file path to text')
    
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

    logger = get_logger('ParserLogger', args.log_level)
    sents_fp = args.text_file_path

    sents = readf(sents_fp).split("\n")


    logger.info("Parser loading")
    stog = amrlib.load_stog_model()
    logger.info("parsing {}\nplease be patient...".format(args.text_file_path))
    graphs = stog.parse_sents(sents)

    string = "\n\n".join(graphs)

    with open(args.out_file_path,"w") as f:
        f.write(string)
    logger.info("parsing finished, output written to {}".format(args.out_file_path))

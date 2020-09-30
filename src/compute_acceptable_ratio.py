import sys
import data_helpers as dh
import argparse
from log_helper import get_logger

def build_arg_parser():

    parser = argparse.ArgumentParser(
            description='normalize LM assessment to ratio')

    parser.add_argument('-score_file_path'
            , type=str
            , help='file path to text')
    
    parser.add_argument('-ref_score_file_path'
            , type=str
            , help='file path to ref text')

    parser.add_argument('-out_file_path'
            , type=str
            , default="tmp/out.normalized-lm-prob"
            , help='file path to out preds')

    parser.add_argument('-tolerance'
            , type=float
            , default=0.05
            , nargs = '?'
            , help='tolerance parameter: acceptable if \
                    score(sent) / (score(ref) + score(sent)\
                    >= 0.5 - tolerance')
    
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
    logger = get_logger("AcceptableRatioLogger",args.log_level)

    genp = args.score_file_path
    refp = args.ref_score_file_path

    string_gen = dh.readf(genp)
    string_ref = dh.readf(refp)

    scores_gen = [float(x) for x in string_gen.split("\n")]
    scores_ref = [float(x) for x in string_ref.split("\n")]

    num = 0
    denom = 0
    logger.info("computing accepatility level corpus score for {}...".format(
        args.score_file_path))
    for i, score in enumerate(scores_gen):
        score_ref = scores_ref[i]

        prefer_prob = score / (score + score_ref)

        
        if prefer_prob >= 0.5 - args.tolerance:
            num += 1
        denom += 1
        logger.debug("sentence idx {};\
                score generated={};\
                score ref={};\
                preference score={};\
                preference score minus tol={};\
                acceptable={}".format(i
                    , score
                    , score_ref
                    , prefer_prob
                    , prefer_prob - args.tolerance
                    , prefer_prob >= 0.5 - args.tolerance))

    with open(args.out_file_path, "w") as f:
        f.write("acceptable ratio: {}".format(num/denom))
    
    logger.info("finished... writing output to {}".format(args.out_file_path))

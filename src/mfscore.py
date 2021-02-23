import data_helpers as dh
import sys
import argparse
from log_helper import get_logger

def build_arg_parser():

    parser = argparse.ArgumentParser(
            description='compute final MFscore')

    parser.add_argument('-form_score_file_path'
            , type=str
            , help='file path to file with acceptable sentence ratio')

    parser.add_argument('-meaning_score_file_path'
            , type=str
            , help='file path to file with S(2)match score')
    
    parser.add_argument('-output_file_path'
            , type=str
            , nargs="?"
            , default="../evaluation-reports/report.txt"
            , help='file path output evaluation report')

    parser.add_argument('-log_level'
            , type=int
            , nargs='?'
            , default=10
            , choices=list(range(0,60,10))
            , help='logging level (int), see\
                    https://docs.python.org/3/library/logging.html#logging-levels')

    return parser

def get_score(string, filterf = lambda string:string):
    #Document F-score: 0.480, 0.4800
    string = filterf(string)
    sm = float(string)
    return sm

def mf_beta_score(meaning, form, beta):
    num = (1 + beta * beta) * meaning * form
    denom = beta * beta * meaning + form
    return num / denom

if __name__ == "__main__":
    args = build_arg_parser().parse_args()
    logger = get_logger("MFscoreLogger", args.log_level)
    logger.info("loading scores from files {} & {} to compute MF score".format(
        args.meaning_score_file_path, args.form_score_file_path))
    mstring = dh.readf(args.meaning_score_file_path)
    fstring = dh.readf(args.form_score_file_path)
    meaning = get_score(mstring, filterf = lambda string: string.split(", ")[1])
    form = get_score(fstring, filterf = lambda string: string.split("ratio: ")[1])

    strings = ["Evaluation Result"]
    strings.append("-" * (len(strings)-1) )

    strings.append("MF(\\beta=1), harm. mean of Form and Meaning:\n----> {}\n\n".format(
        mf_beta_score(meaning, form, 1)))
    strings.append("MF(\\beta=0.5), Meaning is double important:\n----> {}\n\n".format(
        mf_beta_score(meaning, form, 0.5)))
    strings.append("MF(\\beta=2), Form is double important:\n----> {}\n\n".format(
        mf_beta_score(meaning, form, 2)))
    strings.append("MF(\\beta -> 0), Meaning score:\n----> {}\n\n".format(
        meaning))
    strings.append("MF(\\beta -> infinity), Form score:\n----> {}\n\n".format(form))
    string = "\n".join(strings)
    dh.writef(string,args.output_file_path)
    logger.info("Successfully computed MF score, saving report to {}".format(
        args.output_file_path))

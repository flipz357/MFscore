#!/usr/bin/env bash

LM="gpt2"
LOGLEVEL=20

PATH_GEN=$1
PATH_AMR_REF=$2
PATH_REF=$3

FILE_GEN=$(basename $PATH_GEN)
FILE_AMR=$(basename $PATH_AMR_REF)


cd src
python clean.py \
    -generated_text_file_path ../$PATH_GEN \
    -source_amr_file_path ../$PATH_AMR_REF \
    -out_file_path tmp/$FILE_GEN.clean \
    -out_file_path_ref_sents tmp/$FILE_AMR-sents.clean \
    -acronym_file_paths ../data/dict/country_adjectivals.txt \
    -log_level $LOGLEVEL


python parse.py -text_file_path tmp/$FILE_GEN.clean \
    -out_file_path tmp/$FILE_GEN.clean.stog_parsed \
    -log_level $LOGLEVEL


/opt/slurm/bin/srun -p compute --mem=30000 python score_form_per_sent.py \
    -text_file_path tmp/$FILE_GEN.clean \
    -out_file_path tmp/$FILE_GEN.clean.lm_score-$LM \
    -LM $LM \
    -log_level $LOGLEVEL

/opt/slurm/bin/srun -p compute --mem=30000 python score_form_per_sent.py \
    -text_file_path tmp/$FILE_AMR-sents.clean \
    -out_file_path tmp/$FILE_AMR-sents.clean.lm_score-$LM \
    -LM $LM \
    -log_level $LOGLEVEL


python compute_acceptable_ratio.py \
    -score_file_path tmp/$FILE_GEN.clean.lm_score-$LM \
    -ref_score_file_path tmp/$FILE_AMR-sents.clean.lm_score-$LM \
    -out_file_path tmp/$FILE_GEN-vs-$FILE_AMR-sents.lm_score-$LM.normalized \
    -tolerance 0.05 \
    -log_level $LOGLEVEL

cd ..

cd amr-metric-suite/py3-Smatch-and-S2match/smatch/

python s2match.py -f ../../../src/tmp/$FILE_GEN.clean.stog_parsed ../../../$PATH_AMR_REF \
    -vectors ../../vectors/glove.6B.100d.txt \
    > ../../../src/tmp/$FILE_GEN-vs-$FILE_AMR.s2match

cd ../../../src


python mfscore.py \
    -meaning_score_file_path tmp/$FILE_GEN-vs-$FILE_AMR.s2match \
    -form_score_file_path tmp/$FILE_GEN-vs-$FILE_AMR-sents.lm_score-$LM.normalized \
    -log_level $LOGLEVEL 

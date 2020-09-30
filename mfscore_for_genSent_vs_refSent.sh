#!/usr/bin/env bash

LM="gpt2"
LOGLEVEL=20

PATH_GEN=$1
PATH_REF=$2

FILE_GEN=$(basename $PATH_GEN)
FILE_REF=$(basename $PATH_REF)


cd src
python clean.py \
    -generated_text_file_path ../$PATH_GEN \
    -out_file_path tmp/$FILE_GEN.clean \
    -acronym_file_paths ../data/dict/country_adjectivals.txt \
    -log_level $LOGLEVEL \

python clean.py \
    -generated_text_file_path ../$PATH_REF \
    -out_file_path tmp/$FILE_REF.clean \
    -acronym_file_paths ../data/dict/country_adjectivals.txt ../data/dict/acronyms.txt \
    -log_level $LOGLEVEL 


python parse.py -text_file_path tmp/$FILE_GEN.clean \
    -out_file_path tmp/$FILE_GEN.clean.stog_parsed \
    -log_level $LOGLEVEL 

python parse.py -text_file_path tmp/$FILE_REF.clean \
    -out_file_path tmp/$FILE_REF.clean.stog_parsed \
    -log_level $LOGLEVEL 


/opt/slurm/bin/srun -p compute --mem=30000 python score_form_per_sent.py \
    -text_file_path tmp/$FILE_GEN.clean \
    -out_file_path tmp/$FILE_GEN.clean.lm_score-$LM \
    -LM $LM \
    -log_level $LOGLEVEL 

/opt/slurm/bin/srun -p compute --mem=30000 python score_form_per_sent.py \
    -text_file_path tmp/$FILE_REF.clean \
    -out_file_path tmp/$FILE_REF.clean.lm_score-$LM \
    -LM $LM \
    -log_level $LOGLEVEL 


python compute_acceptable_ratio.py \
    -score_file_path tmp/$FILE_GEN.clean.lm_score-$LM \
    -ref_score_file_path tmp/$FILE_REF.clean.lm_score-$LM \
    -out_file_path tmp/$FILE_GEN-vs-$FILE_REF.lm_score-$LM.normalized \
    -tolerance 0.05 \
    -log_level $LOGLEVEL 

cd ..

cd amr-metric-suite/py3-Smatch-and-S2match/smatch/

/opt/slurm/bin/srun -p compute --mem=30000 python s2match.py -f ../../../src/tmp/$FILE_GEN.clean.stog_parsed ../../../src/tmp/$FILE_REF.clean.stog_parsed \
    -vectors ../../vectors/glove.6B.100d.txt \
    > ../../../src/tmp/$FILE_GEN-vs-$FILE_REF.s2match

cd ../../../src

python mfscore.py \
    -meaning_score_file_path tmp/$FILE_GEN-vs-$FILE_REF.s2match \
    -form_score_file_path tmp/$FILE_GEN-vs-$FILE_REF.lm_score-$LM.normalized \
    -log_level $LOGLEVEL 

# MF score for explainable evaluation of text generation

For some teachers, the **Form** of an essay may be important, for others, the **Meaning** may be important. 
Many others take a balanced approach to **Form** and **Meaning**.

This repo **puts you in control of what you expect of your NLG system**: 

Should it excel more in **Form** or more in **Meaning**, or both equally? It's **your choice**. 


## Preparation

We recommend setting up a virtual environment to install the requirements

1. run `pip -r requirements.txt`

2. download spacy model `en_core_web_sm`  (it's used for true-casing)

3. clone [amrlib](https://github.com/bjascob/amrlib), isntall it and install a parser model. Follow their instructions (I tested with version `0.0.1`).

4. clone [amr-metric-suite](https://github.com/flipz357/amr-metric-suite) here

## MF score for evaluation of general sentence generation

![Score computation](img/score_pipeline_outline_sent_sent-crop.png)

Simply call:
```
./mfscore_for_genSent_vs_refSent.sh <generated_file> <reference_file>
```
where `<generated_file>` and `<reference_file>` are files that contain one sentence per line. See `example.txt`

## MF score for evaluation of AMR-to-text generation

![Score computation](img/score_pipeline_outline_sent_amr-crop.png)

Simply call:
```
./mfscore_for_genSent_vs_refAMR.sh <generated_file> <reference_file>
```
where `<generated_file>` contains one sentence per line and `<reference_file>` contains AMRs separated by an empty line (standard AMR Sembank, see `example.txt`).



## Additional information

If you want to run the fine grained semantic evaluation (e.g., how good is your generated text w.r.t. to coreference?), run

```
./fined_grained_semantic_analyis.sh <amr-file-pred> <amr-file-ref>
```

where both input files are AMR corpora (AMRs separated by an empty line, standard AMR Sembank, see `example.txt`). Chances are that you have already generated them when using the MF score, please look in `src/tmp/`.

### Citation

If you like our idea, please consider citing

```
@article{opitz2020towards,
  title={Towards a Decomposable Metric for Explainable Evaluation of Text Generation from AMR},
  author={Opitz, Juri and Frank, Anette},
  journal={arXiv preprint arXiv:2008.08896},
  year={2020}
}
```

### Change log

* version 0.0.1 released

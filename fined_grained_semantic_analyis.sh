#!/usr/bin/env bash

PATH_GENAMR=$(realpath $1)
PATH_REFAMR=$(realpath $2)

cd amr-metric-suite/py3-Smatch-and-S2match

./evaluation-fixed-s2match.sh $PATH_GENAMR $PATH_REFAMR



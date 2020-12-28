# cinnamon
## Introduction
This is a basic project that I'm picking up for funsies during the break. Basically,
the point of this project is to create a bossier life-coach version of Jarvis. 

## Project Setup
DISCLAIMER: Because of an issue with the way tensorflow's keras saves and loads
models from h5 files, I had to modify the keras package's source code. This issue
is detailed here: https://github.com/tensorflow/tensorflow/issues/44467. The
project fails to load the model from the h5 file if instances of `.decode('utf-8')`
are not removed from `python3.9/site-packages/tensorflow/python/keras/engine/saving.py`.

## Citations
Training data courtesy of https://www.kaggle.com/praveengovi/emotions-dataset-for-nlp
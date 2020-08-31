# Soliloquy Web Demo

A web demo of utterance variation approaches. Currently, neural paraphrasing 
with T5 is implemented.

Running without a GPU is slow, especially with files with more than 50 lines.

### Requires the following python 3 packages (install with pip3)

- bottle
- numpy
- pandas
- pytorch-lightning (for training only)
- sentencepiece
- torch
- transformers

### Running

On a linux machine, clone the repository, enter the main directory and type:

`sudo python3 demo.py`

### Models

A model is not included. Download pytorch_model.bin from https://ucdavis.box.com/v/soliloquy (password required),
and place it in the paraphrase/quora_paws_model directory.

# DS 101 Guest lecture materials

This repository contains the materials for the guest lecture on LLMs and RAG for the course DS 101 at the College of Charleston 11/20/23

## Slides
[Enhancing_LLMs_with_RAG.pdf](Enhancing_LLMs_with_RAG.pdf)

## Files Description

`extract.py` will scape wikipedia and save the results to a json file.  This data is also available for
download at these links 
[texts.json.gz](https://cheesegpt.s3.amazonaws.com/texts.json.gz)
[metadata.json.gz](https://cheesegpt.s3.amazonaws.com/metadata.json.gz)


`load.py` will generate embeddings which costs ~$5 in openAI credits.  I've also uploaded the redis database
including the embeddings so this isn't necessary to run the demo.


`chat.py` contains the code for extracting results from redis db and generating a response from openAI api.
An openAI api key is required to run this code, but its very cheap to run a few examples (less than $0.10)

## Project Setup
Install using pip
```
pip install -r requirements.txt
```
or poetry 
```
poetry install
```
Store your openAI api key in `.env` file

## Setup and Run

run `sh download_and_init_nev.sh` to download the rds database and initialize the redis server

Once your docker logs print `Ready to accept connections tcp`, you should be able to execute the code in `chat.py` now and create additional examples.


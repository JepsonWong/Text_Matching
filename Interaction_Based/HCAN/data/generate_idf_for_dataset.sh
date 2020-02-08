#!/bin/bash

for dataset in "./data/dataset/TrecQA" "./data/dataset/Quora" "./data/dataset/TwitterURL"
    do
    echo ">>> Build IDF weights for ${dataset}"
    python -u ./data/generate_idf_for_dataset.py -d ${dataset}
done

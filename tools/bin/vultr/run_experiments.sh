#!/bin/bash
mkdir -p ~/src/nt-recommend/data/results/
cd ~/src/nt-recommend/src

# mean predictor

python3 manage.py mean_predictor 
sleep 10

python3 manage.py mean_predictor --kn 10 
sleep 10



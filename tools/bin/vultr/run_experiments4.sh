#!/bin/bash
mkdir -p ~/src/nt-recommend/data/results/
cd ~/src/nt-recommend/src

# collaborative filtering

python3 manage.py collaborative_filter --m msd --ns 10
sleep 10

python3 manage.py collaborative_filter --m pearson --ns 10
sleep 10


python3 manage.py collaborative_filter --m msd --ns 10 --kn 10
sleep 10
#!/bin/bash
mkdir -p ~/src/nt-recommend/data/results/
cd ~/src/nt-recommend/src

# mean predictor

python3 manage.py mean_predictor >> ~/src/nt-recommend/data/results/results.txt
sleep 10

python3 manage.py mean_predictor --kn 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10


# collaborative filtering

python3 manage.py collaborative_filter --m msd --ns 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10

python3 manage.py collaborative_filter --m pearson --ns 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10


python3 manage.py collaborative_filter --m msd --ns 10 --kn 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10

python3 manage.py collaborative_filter --m pearson --ns 10 --kn 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10


python3 manage.py collaborative_filter --m msd --ns 100 --kn 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10

python3 manage.py collaborative_filter --m pearson --ns 100 --kn 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10


# resnik collaborative filtering


python3 manage.py resnik_collaborative_filter  --m msd --ns 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10

python3 manage.py resnik_collaborative_filter  --m pearson --ns 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10

python3 manage.py resnik_collaborative_filter  --m pearson --ns 10 --kn 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10


python3 manage.py resnik_collaborative_filter  --m msd --ns 100 >> ~/src/nt-recommend/data/results/results.txt
sleep 10

python3 manage.py resnik_collaborative_filter  --m pearson --ns 100 >> ~/src/nt-recommend/data/results/results.txt
sleep 10

python3 manage.py resnik_collaborative_filter  --m pearson --ns 100 --kn 10 >> ~/src/nt-recommend/data/results/results.txt
sleep 10

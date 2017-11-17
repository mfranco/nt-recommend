#!/bin/bash

cd ~/src/nt-recommend/src
python3 manage.py resnik_collaborative_filter  --m msd --ns 10 >> ~/src/nt-recommend/data/results/resnik.txt
python3 manage.py resnik_collaborative_filter  --m pearson --ns 10 >> ~/src/nt-recommend/data/results/resnik.txt
python3 manage.py resnik_collaborative_filter  --m msd --ns 100 >> ~/src/nt-recommend/data/results/resnik.txt
python3 manage.py resnik_collaborative_filter  --m pearson --ns 100 >> ~/src/nt-recommend/data/results/resnik.txt

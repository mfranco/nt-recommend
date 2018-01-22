#!/bin/bash
mkdir -p ~/src/nt-recommend/data/results/
cd ~/src/nt-recommend/src

# leave one out for recommenders

python3 manage.py frequent_item_recommender --ns 10 --m pearson
sleep 10

python3 manage.py frequent_item_recommender --ns 100 --m pearson
sleep 10

python3 manage.py linked_item_recommender --ns 10  --m pearson
sleep 10


python3 manage.py linked_item_recommender --ns 100  --m pearson
sleep 10


python3 manage.py mean_predictor_recommender --ns 10  --m pearson
sleep 10


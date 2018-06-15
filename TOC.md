# Table of Contents / File Directory


## Model notebooks

JGT_model_5.ipynb:  Final logistic-regression model with some anlysis of cost-benefit  
JGT_model_4.ipynb:  Penultimate logistic-regression models  
JGT_model_3.ipynb:  Support-vector-machine models, which overfit  
JGT_models_2.ipynb:  AdaBoost and RandomForest, never optimized  
JGT_models.ipynb:  AdaBoost and RandomForest, never optimized  


## EDA notebooks

JGT_EDA.ipynb:  EDA on weather data, some feature engineering  
EDA-train-test-JW.ipynb: EDA on training and test data, some feature engineering and modeling

* additional material found at https://public.tableau.com/profile/jon.withers#!/vizhome/chicagownv/Sheet8 *

## Utility scripts

utilities/import-and-clean.py: Contains functions to input and prepare data, including all features used in models. When executed, reproduces the training and test data used in model notebooks.  
utilities/ensemble.py:  Contains functions to put three classifiers together in an sklearn VotingClassifier and gridsearch over weights  
utilities/lat_lon_ds.py:  Contains functions to find distance between two (lat, lon) coordinates, tuned for the Chicago area  
utilities/JGT_engineered_features.py:  Functions to create engineered features based on weather data  


## Input data

assets/master_clean_train.csv:  Cleaned data set.  'train.csv' joined to engineered features  
assets/master_clean_test.csv:  Cleaned data set.  'train.csv' joined to engineered features  


## Output data

output/kagglesubmission_<date time>.csv: model predictions (from JGT_model_4.ipynb or JGT_model_5.ipynb), formatted for submission to Kaggle  
output_log.txt:  Tracks submission files  


## Planning documents

Action Items.md:  living document, tracks issues  
Roles.md:  Documents division of labor among team members, roughly.  


## Misc

assets/input/*.*: files from Kaggle  
assets/src/*.*: files from Kaggle  
assets/visualizations/*.*: visualizations generated from EDA and external sources  

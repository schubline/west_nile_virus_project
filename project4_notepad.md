## This is a general-purpose notepad for project 4, group2

### 2018-6-4

Perhaps we should train three models on three different sets of features and then ensemble them somehow?
This will require some method for ad hoc ensemble.  Perhaps one works on weather, one works on spraying, one works on trap data?

Work on each classifier in parallel until it is determined that a classifier is complete, or should be abandoned or sgoudl be combined with another classifier, etc., then re-allocate staff.

#### pseudopseudocode

Put all data into a dataframe or dataframes
  Clean it, join it, etc.
  Make sure this is ultimately embodied in a function, so we can conveniently put the test data through the same pipeline
  
EDA
  Get basic stats, whatever you like
  Build a baseline model and run it

Build trap classifier
  Uses train.csv
  Should have a method to give equivalent of 'predict_proba' on any observation in test set
  idealy, this will be a single function

Build weather classifier
   Uses weather.csv
   Should have a method to give equivalent of 'predict_proba' on  any observation in test set
   idealy, this will be a single function

Build spray classifier
   Uses spray.csv
   Should have a method to give equivalent of 'predict_proba' on  any observation in test set
   idealy, this will be a single function

Build the ensemble classifier
  Somehow synthesize the predictions
  ideally, this will be a single function

Posprocessing
  Output predictions for test data into CSV



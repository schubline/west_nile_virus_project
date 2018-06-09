# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 10:23:24 2018

@author: James
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def ensemble_p(X, model_list, weight_list):
    """Weighted average of model predictions.  Models are sklearn objects in a
    list 'model_list'.  They are classifiers with method 'predict_proba()'
    Weights are in list 'weight_list'.  Each weight is 0 < w < 1, and together
    they add to 1.
    """
    
    # Initialize probability
    p = 0
    
    # Add up the predictions in a loop
    for m, w in zip(model_list, weight_list):
        p += m.predict_proba(X)*w

    return p

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def ensemble_two_models(X, y, model_list):

    from sklearn.ensemble import VotingClassifier
    from sklearn.model_selection import GridSearchCV
    from sklearn.ensemble import RandomForestClassifier
    
    vc = VotingClassifier([('m0', model_list[0]),('m1', model_list[1])],
                           voting='soft')
    
    w1 = np.linspace(0,1,11)
    w2 = 1 - w1
    w_array = [[w_one, w_two] for w_one, w_two in zip(w1,w2)]
    # w1 and w2 are independantly varied.  This will allow a third weight, w3, to 
    # be calculated via 1 = w1 + w2 + w3
    gs_params = {'weights': w_array}
    
    gscv = GridSearchCV(vc, gs_params,
                        cv=5, return_train_score=True)
    gscv.fit(X,y)
    
    return gscv

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

"""
Test rig for GridSerach on ensemble classifier, built w/ iris data
"""


from sklearn.datasets import load_iris

data = load_iris()
y = data.target
X = data.data

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

rfc1 = RandomForestClassifier(n_estimators = 5, max_depth = 3)
rfc2 = RandomForestClassifier(n_estimators = 3, max_depth = 5)

from sklearn.model_selection import GridSearchCV

gscv = ensemble_two_models(X,y, [rfc1, rfc2])

gscv.cv_results_
gscv.best_score_

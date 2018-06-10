# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 10:23:24 2018

@author: James
"""

import numpy as np
import pandas as pd

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
    """Calls GridSearchCV on a VotingCLassifier object.  Grid search 
    is  performed over various weights given to the two estimators in 
    the VotingClassifer.
    
    Parameters:
    ----------
    X:  array of predictor values, formatted for sklearn
    y:  target values, formatted for sklearn
        model_list: a list of two sklearn classifiers
    
    Returns:
    --------
    gscv:   A fitted GridSearchCV object.  Score for each cv 
        is the ROC AUC (only works for binary classes)        
    
    """
    
    from sklearn.ensemble import VotingClassifier
    from sklearn.model_selection import GridSearchCV

    # Probably need to import here all classifier types that 
    # might be sent to this function
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    
    vc = VotingClassifier([('m0', model_list[0]),('m1', model_list[1])],
                           voting='soft')
    
    # put together the parameter list for different weights
    # for the VotingClassifier
    w1 = np.linspace(0,1,11)
    w2 = 1 - w1
    w_array = [[w_one, w_two] for w_one, w_two in zip(w1,w2)]

    
    gs_params = {'weights': w_array}

    gscv = GridSearchCV(vc, gs_params,
                        cv=5, return_train_score=True, scoring = 'roc_auc')
    gscv.fit(X,y)
    
    return gscv

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    

def ensemble_three_models(X, y, model_list):
    """Calls GridSearchCV on a VotingCLassifier object.  Grid search 
    is  performed over various weights given to the two estimators in 
    the VotingClassifer.
    
    Parameters:
    ----------
    X:  array of predictor values, formatted for sklearn
    y:  target values, formatted for sklearn
        model_list: a list of two sklearn classifiers
    
    Returns:
    --------
    gscv:   A fitted GridSearchCV object.  Score for each cv 
        is the ROC AUC (only works for binary classes)        
    
    """
    
    from sklearn.ensemble import VotingClassifier
    from sklearn.model_selection import GridSearchCV

    # Probably need to import here all classifier types that 
    # might be sent to this function
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    
    vc = VotingClassifier([('m0', model_list[0]),
                           ('m1', model_list[1]),
                           ('m2', model_list[2])],
                           voting='soft')
    
    # put together the parameter list for different weights
    # for the VotingClassifier
    grid_size = 4
    w_array = []
    for i in np.linspace(0,1,grid_size):
        for j in np.linspace(0,1,grid_size):
            for k in np.linspace(0,1,grid_size):
                if ((i+j+k) < 1 + 1e-14) and ((i+j+k) > 1 - 1e-14 ):
                    w_array.append([i,j,k])
    
    gs_params = {'weights': w_array}

    gscv = GridSearchCV(vc, gs_params,
                        cv=5, return_train_score=True, scoring = 'roc_auc')
    gscv.fit(X,y)
    
    return gscv

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def CV_test_rig_2rfc(X,y):
    """
    Tests GridSearchCV with a VotingClassifier composed of two 
    RandomForestClassifiers
    
    Parameters:
    ----------
    X: predictors, sklearn format
    y: targets, sklearn format
    
    Returns:
    --------
    gscv: a fitted GridSearchCV object
    """
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import GridSearchCV
    
    rfc1 = RandomForestClassifier(n_estimators = 5, max_depth = 3)
    rfc2 = RandomForestClassifier(n_estimators = 3, max_depth = 5)
    
    from sklearn.model_selection import GridSearchCV
    
    gscv = ensemble_two_models(X,y, [rfc1, rfc2])

    return gscv

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def CV_test_rig_3rfc(X,y):
    """
    Tests GridSearchCV with a VotingClassifier composed of three
    RandomForestClassifiers
    
    Parameters:
    ----------
    X: predictors, sklearn format
    y: targets, sklearn format
    
    Returns:
    --------
    gscv: a fitted GridSearchCV object
    """
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import GridSearchCV
    
    rfc1 = RandomForestClassifier(n_estimators = 5, max_depth = 4)
    rfc2 = RandomForestClassifier(n_estimators = 4, max_depth = 5)
    rfc3 = RandomForestClassifier(n_estimators = 10, max_depth = 2)
    
    from sklearn.model_selection import GridSearchCV
    
    gscv = ensemble_three_models(X,y, [rfc1, rfc2, rfc3])

    return gscv

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


"""
Test rig for GridSearch on ensemble classifier, built w/ breast-cancer
data
"""

from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
y = data.target
X = data.data

gscv = CV_test_rig_3rfc(X,y)

cv_results_df = pd.DataFrame(gscv.cv_results_)
gscv.best_score_
gscv.best_params_

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.model_selection import cross_val_score

import matplotlib.pyplot as plt
import seaborn as sns

master_train = pd.read_csv("assets/master_clean_train.csv", index_col=0)

print("master_train_shape: ", master_train.shape)
print("\n")

master_train['dtdate'] = pd.to_datetime(master_train['dtdate'])

master_train['month'] = master_train['dtdate'].dt.month

master_train = pd.get_dummies(master_train, columns=['month'], drop_first=True)

print("Columns in input dataset: ")
print(list(master_train.columns))

target = 'wnvpresent'
features = ['species_culex_pipiens',
       'species_culex_pipiens_restuans', 'species_culex_restuans',
       'neighborhood_infection_category_high',
       'neighborhood_infection_category_low',
       'neighborhood_infection_category_medium',
       'neighborhood_infection_category_none', 'park_score', 'daylight',
       'avg_tavg', 'avg_preciptotal', 'avg_avgspeed', 'timelaggeddaylight',
       'timelaggedtemperature', 'timelaggedprecipitation',
       'timelaggedwindspeed', 'month_6', 'month_7', 'month_8', 'month_9',
       'month_10']
X = master_train[features]
y = master_train[target]

print(" ")
print("Features and types:")
print(X.dtypes, "\n--------")

sm = SMOTE()

X_res, y_res = sm.fit_sample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_res, y_res)

ss = StandardScaler()

X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

supvec = SVC(probability=True)


supvec.fit(X_train, y_train)
print("SVC results: ")
print("Cross-val score: ", cross_val_score(supvec, X_train, y_train, cv = 5, scoring="roc_auc"))
print(" ")
print("Test score: ", roc_auc_score(y_test, supvec.predict(X_test)))

predictions = supvec.predict_proba(X_test)

pos_predictions = [i[1] for i in predictions]

sns.heatmap(confusion_matrix(y_test, supvec.predict(X_test)), annot = True, fmt = "g")
plt.title("Confusion Matrix for SVM model", fontsize = 18)
plt.show()
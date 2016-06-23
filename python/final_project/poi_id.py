#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".

# Let's use all features currently, except 'email_address' which is useless
fin_features = ['salary', 'bonus', 'total_stock_value', 'exercised_stock_options']
em_features = ['shared_receipt_with_poi']

# Concat 2 lists
### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

    
### Task 2: Remove outliers
# Let's remove 1 outlier of which we are sure
data_dict.pop('TOTAL', 0)
data_dict.pop('THE TRAVEL AGENCY IN THE PARK', 0)
#for i in data_dict:
#    print data_dict[i]['other']

### Store to my_dataset for easy export below.
my_dataset = data_dict
#print my_dataset

### Task 3: Create new feature(s)
# Need to introduce percent of emails sent to poi & persent of emails received from poi
import math
for i in my_dataset:
    my_dataset[i]['to_poi_ratio'] = float(my_dataset[i]['from_this_person_to_poi']) / float(my_dataset[i]['from_messages'])
    my_dataset[i]['to_poi_ratio'] = "NaN" if math.isnan(my_dataset[i]['to_poi_ratio']) else my_dataset[i]['to_poi_ratio']

# Reduce email features
from sklearn.feature_selection import SelectKBest
em_features = em_features + ['to_poi_ratio']
# data_em = featureFormat(my_dataset, ['poi'] + em_features, sort_keys = True)
# labels_em, features_em = targetFeatureSplit(data_em)
# k_email = SelectKBest(k=2)
# k_email.fit_transform(features_em, labels_em)
# print k_email.scores_


# Reduce fin features
# data_fin = featureFormat(my_dataset, ['poi'] + fin_features, sort_keys = True)
# labels_fin, features_fin = targetFeatureSplit(data_fin)
# k_fin = SelectKBest(k=5)
# k_fin.fit_transform(features_fin, labels_fin)
# print k_fin.scores_


### Extract features and labels from dataset for local testing
features_list = ['poi'] + fin_features + em_features
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# Scale the data
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Example starting point. Try investigating other evaluation techniques!
# Split the data
from sklearn.cross_validation import train_test_split
#features_train, features_test, labels_train, labels_test = \
#    train_test_split(features, labels, test_size=0.3, random_state=42)

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
#estimators = [('pca', RandomizedPCA()), ('forest', AdaBoostClassifier())]
#clf = Pipeline(estimators)
#clf.set_params(pca__n_components=2, forest__base_estimator=RandomForestClassifier(n_estimators=3, criterion='entropy', max_depth=5))    

#from sklearn.metrics import precision_recall_curve
from sklearn.metrics import precision_score, fbeta_score, recall_score
from sklearn.metrics import make_scorer

def custom_scorer(labels, predictions):
    return min(precision_score(labels, predictions), recall_score(labels, predictions))

scorer  = make_scorer(custom_scorer, greater_is_better=True)
from sklearn.svm import SVC
#myscorer = make_scorer(fbeta_score, beta=2)

estimators = [#('pick', SelectKBest()),
              #('scale', MinMaxScaler(copy=False)),
#              ('scale', StandardScaler(copy=False)),
              ('pca', PCA(copy=False, n_components=4)),
              ('tree', (DecisionTreeClassifier(random_state=42, max_features='sqrt', max_depth=7)))
#              ('svm1', SVC(kernel='rbf', C=100, gamma=0.5))
]
#print Pipeline(estimators).named_steps['tree'].get_params().keys()
param_grid = {
#    'tree__max_depth': [4, 5, 6, 7, 8],
#    'tree__criterion': ['gini', 'entropy'],
#    'tree__max_depth': [7, 8, 9, 10, 11]
#    'tree__compute_importances': ['True', 'False'],
#    'pick__k': [8, 9],
#    'pick__k': [8],
#    'pca__n_components': [4],
#    'pca__n_components': [3, 4, 5, 6],
#    'svm__kernel': ['linear', 'rbf', 'poly'],
#    'svm__C': [1, 10, 100, 1000]
}
clf = Pipeline(estimators)
#clf = SVC(kernel='linear')
#clf = GridSearchCV( Pipeline(estimators), param_grid, n_jobs=-1, scoring=scorer )


#clf.set_params()
#clf.fit(features_train, labels_train)

#pred = clf.predict(features_test)
#print "Best params: "
#print clf.best_params_
#print clf.best_estimator_.named_steps['pick'].scores_
#print clf.best_estimator_.named_steps['pick'].pvalues_
#print clf.best_estimator_.named_steps['pca'].components_

#print clf.get_params()
#print "Precision = %.2f" % precision_score(labels_test, pred)
#print "Recall = %.2f" % recall_score(labels_test, pred)

# values = [0] * len(clf.best_estimator_.named_steps['pca'].components_[0])
# for i in clf.best_estimator_.named_steps['pca'].components_:
#     for id, j in enumerate(i):
#         values[id] = values[id] + j
# print values

a = True
# Provided to give you a starting point. Try a variety of classifiers.
#    clf = GaussianNB()
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.grid_search import GridSearchCV
#param_grid = {
#    'n_neighbors': [1, 3, 5], #[1, 2, 3, 4, 5],
#    'weights': ['distance', 'uniform'],
#    'algorithm': ['ball_tree', 'kd_tree']#, 'brute']
#}
#clf = GridSearchCV(KNeighborsClassifier(n_jobs=-1), param_grid)
#clf = neighbors.KNeighborsClassifier(2, weights='distance', algorithm = 'ball_tree')

#from sklearn.cluster import KMeans
#clf = KMeans(n_clusters=2, n_init=100, max_iter=200)
#clf.fit(features)

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

#print labels_train

# Test my clf
from tester import test_classifier
if a == True:
    test_classifier(clf, my_dataset, features_list)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.
dump_classifier_and_data(clf, my_dataset, features_list)

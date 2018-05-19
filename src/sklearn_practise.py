import numpy as np
import pickle
import time

def open_pickle(filename):
    infile = open(filename,'rb')
    opened_pickle = pickle.load(infile)
    infile.close()
    return opened_pickle

data = open_pickle("data")
labels = open_pickle("labels")

start = time.time()
categories = ['neg', 'notr', 'pos']
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
])
text_clf.fit(data, labels)
"""
docs_test = data
predicted = text_clf.predict(docs_test)
print(np.mean(predicted == labels))

from sklearn import metrics
print(metrics.classification_report(labels, predicted,
     target_names=categories))

print(metrics.confusion_matrix(labels, predicted))
"""

docs_test = ["Boğaziçi çok güzel bir yer", "Lanet olsun böyle okula", "Okulda poster sunumu yapılacaktır"]
predicted = text_clf.predict(docs_test)

for p in predicted:
    print("predicted " + categories[p])

end = time.time()
print(end - start)

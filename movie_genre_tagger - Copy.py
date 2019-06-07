import sys
import numpy as np

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from collections import defaultdict
# The training data file must be passed as first argument

counts = defaultdict(int)
targets = []
data = []
with open(sys.argv[1], "r") as f:
    for line in f:
        a = line.rstrip("\n").split(" ", 1)
        if a[0].isalpha:
            targets.append(a[0])
            counts[a[0]] = counts[a[0]] + 1
            data.append(a[1])
f.closed
if not len(data) == len(targets):
    print("data and targets are not the same length")
    exit()

training_size = len(data) 

clf = Pipeline([
            ('vect', CountVectorizer(ngram_range=(1,3))),
            ('tfidf', TfidfTransformer()),
            ('clf', SGDClassifier(loss='hinge', penalty='l2',
                           alpha=1e-3, random_state=42,
                           max_iter=5, tol=None)),
        ])

parameters = {
    'vect__ngram_range': [(1, 1), (1, 2)],
    'tfidf__use_idf': (True, False),
    'clf__alpha': (1e-2, 1e-3),
}

train_data = data[:training_size]
train_targets = targets[:training_size]


clf.fit(train_data, train_targets)

titles = []
pred_data = []
genres = []
with open("test_movies", "r", encoding="utf8") as f:
    for line in f:
        a = line.rstrip("\n").split(";")
        title_genre = a[0].rstrip().split(":")
        titles.append(title_genre[0])
        genres.append(title_genre[1])
        pred_data.append(a[1])
f.closed

predicted = clf.predict(pred_data)


for title, labeled_genre,pred_genre in zip(titles, genres,predicted):
    print("{0}: labeled {1}, predicted {2}".format(title,labeled_genre,pred_genre))
print(metrics.classification_report(genres, predicted))

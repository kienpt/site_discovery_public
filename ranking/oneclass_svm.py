import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm

class Oneclass_SVM:
    def __init__(self, seeds, representation):
        self.text_type = representation

        self.seeds = seeds
        self.clf = svm.OneClassSVM(nu=0.1, kernel="linear", gamma=0.1)
        mdf = max(2/float(len(seeds)), 0.1)  
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_df=1.0, min_df=mdf, use_idf=False)

        self._train_classifier()

    def _train_classifier(self):
        """
        Fit vectorizer and classifier
        """
        print "Fitting vectorizer and classifier..."
        docs = [] # list of strings
        for w in self.seeds:
            docs.extend([p.get_text(self.text_type) for p in w])

        self.vectorizer.fit(docs) 
        train = [w.get_vsm(self.vectorizer, self.text_type) for w in self.seeds]

        # fit the model
        self.clf.fit(train)        

    def update_seeds(self, new_seeds):
        self.seeds.extend(new_seeds)
        for s in self.seeds:
            s.clear()
        self._train_classifier()

    def score(self, websites): 
        print "Scoring..."
        results = []

        X = [w.get_vsm(self.vectorizer, self.text_type) for w in websites]

        scores = self.clf.decision_function(X)
        for i in xrange(len(websites)):
            results.append((websites[i], scores[i])) 
        return results

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from  sklearn.svm import SVC

class ClassifierRanker:
    def __init__(self, pos_sites, representation, neg_sites):
        ratio = 2 # negatives to positives
        self.text_type = representation

        mdf = max(2/float(len(pos_sites)), 0.1)  
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_df=1.0, min_df=mdf, use_idf=True)
        #self.clf = SVC(kernel="linear", probability=True, shrinking=True)
        self.clf = LogisticRegression()

        self.pos_sites, self.neg_sites = pos_sites, neg_sites
        max_neg = min(ratio*len(self.pos_sites), len(neg_sites))
        self.neg_sites = self.neg_sites[:max_neg]

        self._train_classifier()

    def _train_classifier(self):
        """
        Update self.vectorizer and self.clf
        """
        print "Fitting vectorizer and classifier..."
        docs = [] # list of strings
        for w in self.pos_sites:
            docs.extend([p.get_text(self.text_type) for p in w])

        for w in self.neg_sites:
            docs.extend([p.get_text(self.text_type) for p in w])

        self.vectorizer.fit(docs) 

        pos = np.array([w.get_clf_vsm(self.vectorizer, self.text_type) for w in self.pos_sites])
        neg = np.array([w.get_clf_vsm(self.vectorizer, self.text_type) for w in self.neg_sites])
        print "pos", pos.shape
        print "neg", neg.shape
        x = np.concatenate((pos, neg))
        y = np.array([1]*pos.shape[0] + [-1]*neg.shape[0])
        print "Number of positive examples: ", len(pos)
        print "Number of negative examples: ", len(neg)

        # fit the model
        self.clf.fit(x, y)       

    def update_seeds(self, new_seeds):
        self.pos_sites.extend(new_seeds) 
        for s in self.pos_sites:
            s.clear()
        for s in self.neg_sites:
            s.clear()

        self._train_classifier()

    def score(self, websites): 
        print "Scoring..."
        results = []

        X = [w.get_clf_vsm(self.vectorizer, self.text_type) for w in websites]

        scores = self.clf.decision_function(X)
        for i in xrange(len(websites)):
            results.append((websites[i], scores[i])) 
        return results

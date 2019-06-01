import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import svmlight
import numpy as np
import copy

class PULearning(object):
    """
    PULearning using Biased SVM (Bing Liu's ICDM paper)
    """
    def __init__(self, pos_sites, representation, neg_sites):
        ratio = 2 # negatives to positives

        self.text_type = representation
        
        self.pos_sites, self.neg_sites = pos_sites, neg_sites
        max_neg = min(ratio*len(pos_sites), len(neg_sites))
        self.neg_sites = copy.deepcopy(self.neg_sites[:max_neg])
        mdf = max(2/float(len(pos_sites)), 0.1)  
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_df=1.0, min_df=mdf, use_idf=True)

        self.clf = None
        self._train_classifier()

    def _train_classifier(self):
        print "Training classifier..."
        docs = [] # list of strings
        for w in self.pos_sites:
            docs.extend([p.get_text(self.text_type) for p in w])
        for w in self.neg_sites:
            docs.extend([p.get_text(self.text_type) for p in w])
        self.vectorizer.fit(docs) 
        print self.vectorizer.vocabulary_
        
        pos = np.array([w.get_vsm(self.vectorizer, self.text_type) for w in self.pos_sites])
        pos = self._convert_to_svmlight(pos, 1)
        neg = np.array([w.get_vsm(self.vectorizer, self.text_type) for w in self.neg_sites])
        neg = self._convert_to_svmlight(neg, -1)
        train = pos + neg
        print "Number of pos: ", len(pos)
        print "Number of neg: ", len(neg)

        #self.clf = svmlight.learn(train, type='classification', verbosity=0, cost_ratio=0.10, C=10)
        self.clf = svmlight.learn(train, type='classification', C=0.01, cost_ratio=2.0, verbosity=0)

    def update_seeds(self, new_seeds):
        self.pos_sites.extend(new_seeds)
        for s in self.pos_sites:
            s.clear()
        self._train_classifier()

    def score(self, websites): 
        """
        Note: Use all unlabelled websites as negatives but no more than 20x the positives """
        """
        neg = np.array([w.get_vsm(self.vectorizer, self.text_type) for w in websites])
        neg = self._convert_to_svmlight(neg, -1)

        if not self.model:
            max_neg = min(20*len(self.pos), len(neg))
            train = neg[:max_neg]
            print "Number of unlabelled examples: ", len(train)
            print "Training the classifier..."
            train.extend(self.pos) 
            self.model = svmlight.learn(train, type='classification', verbosity=0, cost_ratio=self.cost_ratio, C=self.c)
        """
        print "Scoring..."
        if not self.clf:
            print "Error. Classifier must be trained"
        test = np.array([w.get_vsm(self.vectorizer, self.text_type) for w in websites])
        test = self._convert_to_svmlight(test, -1) # The label does not matter 
        predicts = svmlight.classify(self.clf, test)
        results = [(websites[i], predicts[i]) for i in xrange(len(websites))]
        return results

    def _convert_to_svmlight(self, vects, label):
        """
        Convert dense numpy vectors to data format for svmlight
        svmlight format:
            (<label>, [(<feature_id>, <value>), ...])
        """
        result = []
        for a in vects:
            #features = [(i, a[i]) for i in xrange(len(a)) if a[i]]
            features = [(i, a[i]) for i in xrange(len(a)) if a[i]]
            result.append((label, features))
        return result

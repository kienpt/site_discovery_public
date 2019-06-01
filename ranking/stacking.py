import numpy as np
import copy

from jaccard_similarity import Jaccard_Similarity
from cosine_similarity import Cosine_Similarity
from random_similarity import Random_Similarity
from bayesian_sets import Bayesian_Sets
from oneclass_svm import Oneclass_SVM
from pu_learning import PULearning
from classifier_ranker import ClassifierRanker
from collections import defaultdict


class StackingRanker:
    def __init__(self, seeds, representation, neg_sites, value_type):
        methods = ['bayesian_tfidf', 'classifier', 'cosine', 'jaccard']
        #methods = ['bayesian_tfidf', 'classifier', 'jaccard']
        self.seeds = seeds
        self.representation = representation
        self.neg_sites = neg_sites

        self.stack = []
        for method in methods:
            self.stack.append(self._get_ranker(method))

        self.value_type = value_type

    def _get_ranker(self, scoring):
        if scoring=="pu_learning":
            ranker = PULearning(self.seeds, self.representation, self.neg_sites)
        elif scoring=="jaccard":
            print "Use jaccard similarity as scoring method"
            ranker = Jaccard_Similarity(self.seeds, self.representation)
        elif scoring=="cosine":
            print "Use cosine similarity as scoring method"
            ranker = Cosine_Similarity(self.seeds, self.representation)
        elif scoring=="bayesian_bin":
            print "Use bayesian sets (binary representation) as scoring method"
            #representation['RANKING_EVALUATION']['BayesianSetType'] = 'binary'
            ranker = Bayesian_Sets(self.seeds, self.representation, value_type="binary")
        elif scoring=="bayesian_tfidf":
            print "Use bayesian sets (tfidf representation) as scoring method"
            #representation['RANKING_EVALUATION']['BayesianSetType'] = 'tfidf'
            ranker = Bayesian_Sets(self.seeds, self.representation, value_type="tfidf")
        elif scoring=="oneclass":
            print "Use One-Class SVM as scoring method"
            ranker = Oneclass_SVM(self.seeds, self.representation)
        elif scoring=="random":
            print "Use random as scoring method"
            ranker = Random_Similarity(self.seeds)
        elif scoring=="classifier":
            print "Use classifier as scoring method"
            ranker = ClassifierRanker(self.seeds, self.representation, self.neg_sites)
        else:
            print "Scoring type is wrong"
            ranker = None
        
        return ranker

    def score(self, websites): 
        site2scores = defaultdict(list)
        for ranker in self.stack:
            scores = ranker.score(websites)
            scores.sort(reverse=True, key=lambda x:x[1])
            for s in scores:
                site2scores[s[0]].append(s[1]) 
                
        #stacked_scores = [(s, sum(site2scores[s])/float(len(site2scores[s]))) for s in site2scores]
        stacked_scores = [(s, self.combine_score(site2scores[s], self.value_type)) for s in site2scores]
        stacked_scores.sort(reverse=True, key=lambda x:x[1])
        return stacked_scores

    def combine_score(self, values, method):
        if method == 'avg':
            return sum(values)/float(len(values))
        elif method == 'rrf':
            k = 60
            score = sum([1/float(k + v) for v in values])
            return -score

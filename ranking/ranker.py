"""
Perform the ranking of the candidate websites
with respect to seed websites   
"""
import sys
sys.path.append("utils")
from urlutility import URLUtility
import heapq
from fetcher import Fetcher
from jaccard_similarity import Jaccard_Similarity
from cosine_similarity import Cosine_Similarity
from random_similarity import Random_Similarity
from bayesian_sets import Bayesian_Sets
from oneclass_svm import Oneclass_SVM
from pu_learning import PULearning
from classifier_ranker import ClassifierRanker
from stacking import StackingRanker
from time import time

class Ranker(object):
    def __init__(self, seeds, representation, scoring="similarity", neg_sites=None):
        self.seeds = seeds

        if scoring=="pu_learning":
            print "Use PU learning as scoring method"
            self.scorer = PULearning(self.seeds, representation, neg_sites)
        elif scoring=="jaccard":
            print "Use jaccard similarity as scoring method"
            self.scorer = Jaccard_Similarity(self.seeds, representation)
        elif scoring=="cosine":
            print "Use cosine similarity as scoring method"
            self.scorer = Cosine_Similarity(self.seeds, representation)
        elif scoring=="bayesian_bin":
            print "Use bayesian sets (binary representation) as scoring method"
            #representation['RANKING_EVALUATION']['BayesianSetType'] = 'binary'
            self.scorer = Bayesian_Sets(self.seeds, representation, value_type="binary")
        elif scoring=="bayesian_tfidf":
            print "Use bayesian sets (tfidf representation) as scoring method"
            #representation['RANKING_EVALUATION']['BayesianSetType'] = 'tfidf'
            self.scorer = Bayesian_Sets(self.seeds, representation, value_type="tfidf")
        elif scoring=="oneclass":
            print "Use One-Class SVM as scoring method"
            self.scorer = Oneclass_SVM(self.seeds, representation)
        elif scoring=="random":
            print "Use random as scoring method"
            self.scorer = Random_Similarity(self.seeds)
        elif scoring=="classifier":
            print "Use classifier as scoring method"
            self.scorer = ClassifierRanker(self.seeds, representation, neg_sites)
        elif scoring=='stacking':
            print "Use stacking as scoring method"
            self.scorer = StackingRanker(self.seeds, representation, neg_sites, value_type='avg') 
        elif scoring=='stacking_rrf':
            print "Use stacking rrf as scoring method"
            self.scorer = StackingRanker(self.seeds, representation, neg_sites, value_type='rrf') 
        else:
            print "Scoring type is wrong. Use similarity as default"
            #self.scorer = Jaccard_Similarity(self.seeds)
            self.scorer = Cosine_Similarity(self.seeds, representation)

    def rank(self, candidates, prf=False):
        """
        Arguments:
            prf: Pseudo-Relevance Feedback

        Return type:
            List of [website, score] sorted by score in descending order
        """
        scores = self.scorer.score(candidates) # scores = list of (website, score)
        scores.sort(reverse=True, key=lambda x:x[1])
        if prf:
            # Add the top k candidates to the seeds 
            print "Reset previous vectorization"
            for s in candidates:
                s.clear()
            print "Reranking"
            k = 10
            top_sites = [item[0] for item in scores[:k]]
            self.scorer.update_seeds(top_sites)
            scores = self.scorer.score(candidates) # scores = list of (website, score)
            scores.sort(reverse=True, key=lambda x:x[1])

        return scores

def test_ranking(seed_file, cand_file, data_dir):
    seed_urls = URLUtility.load_urls(seed_file)
    cand_urls = URLUtility.load_urls(cand_file)

    t = time()
    fetcher = Fetcher(data_dir)
    print "Time to initialize fetcher: ", time()-t
    t = time()
    seeds = fetcher.fetch(seed_urls)
    print "Time to fetch seeds: ",  time()-t
    t = time()
    candidates = fetcher.fetch(cand_urls)
    print "Time to fetch candidates: ", time()-t
    t = time()

    ranker = Ranker(seeds)
    top_sites = ranker.rank(candidates)
    for site, score in top_sites:
        print site.host, score
    print "Time to rank: ", time()-t

if __name__=="__main__":
    seed_file = sys.argv[1]
    cand_file = sys.argv[2]
    data_dir = sys.argv[3]
    test_ranking(seed_file, cand_file, data_dir)

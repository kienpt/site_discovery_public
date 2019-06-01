'''
This class manages the fetched data and ranking new pages with respect to seed pages
'''
import os
import sys
sys.path.append("utils")
import json
from fetcher import Fetcher
from cosine_similarity import Cosine_Similarity
from jaccard_similarity import Jaccard_Similarity
import argparse
import traceback
from urlutility import URLUtility

class Ranking:
    def __init__(self, data_dir, seed_urls, similarity_method):
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        self.fetcher = Fetcher(data_dir)

        if similarity_method == "cosine":
            self.similarity = Cosine_Similarity()
        elif similarity_method == "jaccard":
            self.similarity = Jaccard_Similarity()
        else:
            self.similarity = None
        self.K = max(len(seed_urls)/2, 10)

        self.host = set()
        self.update_seeds(seed_urls)

    def update_seeds(self, seed_urls):
        '''Update seed urls in the current seed list.
        Fetch the seed urls'''
        new_seed_urls = []
        for url in seed_urls:
            host = URLUtility.get_tld(url)
            if host not in self.host:
                self.host.add(host)
                new_seed_urls.append(url)
        urls, text = self.fetcher.fetch_urls(new_seed_urls)
        self.similarity.update_seeds(urls, text)
        self.K = max(len(self.similarity.seed_pages.keys())/2, 10)

    def rank(self, urls):
        ''' Rank the urls with respect to the seeds
            Return the sorted ranking scores together with the urls'''
        # Fetch the urls
        urls, text = self.fetcher.fetch_urls(urls)

        # Rank
        knn_scores = []
        scores = self.similarity.compute_similarity(text) 
        for i in xrange(len(urls)):
            sorted_scores = sorted(scores[i], reverse=True)
            knn_score = sum(sorted_scores[:self.K])/float(min(self.K, len(sorted_scores)))
            knn_scores.append((urls[i], knn_score))
        knn_scores = sorted(knn_scores, key=lambda x:x[1])

        return knn_scores
       

def test(similarity_method):
    print similarity_method
    seed_urls = []
    seed_file = "data/atf/atf_market_places_seeds.txt"
    with open(seed_file) as lines:
        for line in lines:
            seed_urls.append(line.strip())
    ranker = Ranking("data_test", seed_urls, similarity_method) 
    urls = ["http://www.armslist.com/", "http://mit.edu", "http://www.huntingnet.com/forum/"]
    scores = ranker.rank(urls)
    for score in scores:
        print score

if __name__=="__main__":
    test("cosine")
    test("jaccard")

'''
Main class that manages the discovered urls and discovery process
'''
import sys
import os
sys.path.append("ranking")
sys.path.append("search_apis")
from search_apis import Search_APIs
from ranking import Ranking
from url_normalize import url_normalize
from collections import deque
import heapq

import argparse
import traceback

class Discovery:
    def __init__(self, seed_file, data_dir, similarity_method):
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.ranked_urls_file = data_dir + "/ranked_urls.csv"

        self.seed_urls = self._read_urls_from_file(seed_file)
        print "Number of seed urls: ", len(self.seed_urls)
        self.discovered_urls = set()
        for url in self.seed_urls:
            self.discovered_urls.add(url)

        self.searcher = Search_APIs(data_dir)
        self.ranker = Ranking(data_dir, self.seed_urls, similarity_method)
        self.seed_threshold = 0.1 # minimum score for an url to be selected as a seed
        self.search_threshold = 0.05 # minimum score for an url to be selected for search

    def discover_with_backlink_search(self):
        '''url discovery using moz backlink search'''

        next_urls = [(-1.0, url) for url in self.seed_urls]  # negate the scores to turn minheap into maxheap
        heapq.heapify(next_urls) # make next_urls be priority queue
        new_discovered_urls = [] # urls with relevant scores
        ranked_urls = [] # discovered urls with ranking scores

        while next_urls:
            seed = heapq.heappop(next_urls)[1]
            results =  self.searcher.search_related(seed) 
            for url in results:
                if url not in self.discovered_urls:
                    new_discovered_urls.append(url)
                    self.discovered_urls.add(url)

            print "Seed: ", seed, "Retrieved ", len(results), " related urls"

            # Rank the discovered urls
            new_seed_urls = []
            if new_discovered_urls:
                new_ranked_urls = self.ranker.rank(new_discovered_urls)
                self._save_ranked_urls(new_ranked_urls)
                ranked_urls.extend(new_ranked_urls)
                for url, score in new_ranked_urls:
                    if score>self.seed_threshold:
                        new_seed_urls.append(url)
                    if score>self.search_threshold:
                        heapq.heappush(next_urls,(-score, url))
                new_discovered_urls = []
                for url, score in new_ranked_urls: print url, score
            self.ranker.update_seeds(new_seed_urls)

            if len(self.discovered_urls)>300: break

    def discover_with_related_search(self):
        '''url discovery using google related search'''

        next_urls = [(-1.0, url) for url in self.seed_urls]  # negate the scores to turn minheap into maxheap
        heapq.heapify(next_urls) # make next_urls be priority queue
        new_discovered_urls = [] # urls with relevant scores
        ranked_urls = [] # discovered urls with ranking scores

        while next_urls:
            seed = heapq.heappop(next_urls)[1]
            results =  self.searcher.search_related(seed) 
            for url in results:
                if url not in self.discovered_urls:
                    new_discovered_urls.append(url)
                    self.discovered_urls.add(url)

            print "Seed: ", seed, "Retrieved ", len(results), " related urls"

            # Rank the discovered urls
            new_seed_urls = []
            if new_discovered_urls:
                new_ranked_urls = self.ranker.rank(new_discovered_urls)
                self._save_ranked_urls(new_ranked_urls)
                ranked_urls.extend(new_ranked_urls)
                for url, score in new_ranked_urls:
                    if score>self.seed_threshold:
                        new_seed_urls.append(url)
                    if score>self.search_threshold:
                        heapq.heappush(next_urls,(-score, url))
                new_discovered_urls = []
                for url, score in new_ranked_urls: print url, score
            self.ranker.update_seeds(new_seed_urls)

            if len(self.discovered_urls)>300: break
        
    def _save_ranked_urls(self, urls):
        out = open(self.ranked_urls_file, "a+")
        for url, score in urls:
            out.write(str(score) + " " + url + "\n") 
        out.close()

    def test_discover_with_related_search(self):
        '''A simple discovery round using related search'''

        # Discover related urls
        related_urls = [] # results from related search
        for seed in self.seed_urls: 
            results =  self.searcher.search_related(seed) 
            #time.sleep(5)
            if results:
                for url in results:
                    if url not in self.discovered_urls:
                        related_urls.append(url)
                        self.discovered_urls.add(url)

        print "Retrieved ", len(related_urls), " related urls"

        # Rank the discovered urls
        ranked_urls = self.ranker.rank(related_urls)
        for url, score in ranked_urls:
            print url, score

    def _read_urls_from_file(self, filepath):
        urls = []
        with open(filepath) as lines:
            for line in lines:
                url = url_normalize(line.strip())
                urls.append(url) 
        return urls

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--seedfile", help="input file that contains list of seed urls", type=str)
    parser.add_argument("-d", "--data_dir", help="directory that contains the data", type=str)
    parser.add_argument("-s", "--similarity", help="similarity method: jaccard, cosine", type=str)

    args = parser.parse_args()
    parser.print_help()

    discovery = Discovery(args.seedfile, args.data_dir, args.similarity)
    discovery.discover_with_related_search()

if __name__=="__main__" :
    run()

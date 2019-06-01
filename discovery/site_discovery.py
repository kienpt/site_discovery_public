import sys
import json
import time
import math
import argparse
import traceback

sys.path.append("utils")
sys.path.append("ranking")
sys.path.append("search_apis")
from ucb1 import UCB1
from ranker import Ranker
from ranking import Ranking
from urlutility import URLUtility
from search_apis import Search_APIs
from multiproc_fetcher import Fetcher


class SiteDiscovery(object):
    def __init__(self, seed_file, result_file, data_dir):
        """
        Args:
            seed_file: contains list of seed urls
            data_dir: stores crawled data
            result_file: stores urls and their scores
        """
        self.train_urls = URLUtility.load_urls(seed_file)
        self.fetcher = Fetcher(data_dir, None, False) # Note: Fetcher contains Bing Search but does not use it (just for website ranking evaluation)
        self.result_file = result_file
        self.ranked_result_file = result_file + ".rank"
        self.searcher = Search_APIs(data_dir, self.fetcher)

    def get_top_ranked_urls(self, scores, k, selected_urls = set(), site_mode=False):
        """
        Return top k websites that have highest scores and were not selected before
       
        Args:
        - scores: must be sorted by scores descendingly
        - site_mode: If True, get top sites, otherwise get top urls. True is set when searchop == 'bl' or 'rl'
        """
        seed_sites = []
        for i, site_score in enumerate(scores):
            site, score = site_score[0], site_score[1]
            if len(seed_sites)<k:
                if site_mode:
                    url = site.get_host()
                else:
                    url = site.get_url()
                if url not in selected_urls:
                    seed_sites.append(site)
                    selected_urls.add(url)
        return seed_sites

    def save_urls(self, sites, iteration=0):
        out = open(self.result_file, 'a+')
        for i, site in enumerate(sites):
            out.write(site.get_url() + ',' + str(site.get_crawltime()) + ',' + str(iteration) + '\n')
        out.close()

    def save_scores(self, scores):
        out = open(self.ranked_result_file, 'a+')
        for i, site_score in enumerate(scores):
            site, score = site_score[0], site_score[1]
            out.write(site.get_url() + ',' + str(score) +  '\n')
        out.close()

#    def run(self, ranking, selection=None, online=True, max_keyword=10, seed_keyword="gun", kwsearch=False, blsearch=False, rlsearch=False, iters=5, representation='body', negative_file=None):
#        """
#        seed_sites: urls that are used for search
#        selected_urls: urls that were used for search
#        ranked_urls: urls that were ranked 
#
#        Only top-ranked urls will become seed urls
#
#        Args:
#            ranking: str 
#            selection: 'random' or 'search'
#            online: True or False
#        """
#        print "Keyword search enable: ", kwsearch
#        print "Backlink search enable: ", blsearch
#        print "Related search enable: ", rlsearch
#
#        max_pages = 1 # Always use single page to represent a website
#        train_sites = self.fetcher.fetch_sites(self.train_urls, max_pages, selection, online)
#        k = 10 #  number of pages from the newly discovered pages to be added to the seed list
#        #k = 10 #  use 10 for keyword search
#
#        if negative_file: # (random) reliably negative examples
#            neg_urls = URLUtility.load_urls(negative_file)
#            neg_urls = neg_urls[:200]
#        else:
#            neg_urls = []
#        print "neg_urls: ", len(neg_urls)
#        neg_sites = self.fetcher.fetch_sites(neg_urls, 1, None, online)
#        ranker = Ranker(train_sites, representation, ranking, neg_sites)
#        seed_sites = self.train_urls 
#        ranked_urls = set()
#        selected_urls = set() # urls that were used for search
#        for i in xrange(iters):
#            print "\n Iteration ", i
#            seed_sites = [url for url in seed_sites if url not in selected_urls]
#            selected_urls.update(seed_sites)
#
#            print "Searching... ", len(seed_sites), "  seed urls"
#            new_urls = self.searcher.search(seed_sites, related=rlsearch, backlink=blsearch, keyword=kwsearch, seed_keyword=seed_keyword, max_keyword=max_keyword)
#            new_urls = [url for url in new_urls if url not in ranked_urls]
#            ranked_urls.update(new_urls)
#            new_sites = self.fetcher.fetch_sites(new_urls, max_pages, selection, online)
#
#            print "Ranking... ", len(new_sites), " sites"
#            scores = ranker.rank(new_sites)
#            seed_sites = self.get_top_ranked_urls(scores, k)
#
#            self.save_scores(scores, i)

    def run(self, ranking, selection=None, online=True, max_results=50, seed_keyword="gun", searchop="kw", iters=5, representation='body', negative_file=None):
        """
        seed_sites: urls that are used for search
        selected_urls: urls that were used for search

        Only top-ranked urls will become seed urls

        Important Args:
            ranking: a ranking method
            max_results: Maximum number of results to return in related and keyword search
        """
        max_pages = 1 # Always use single page to represent a website
        train_sites = self.fetcher.fetch_sites(self.train_urls, max_pages, selection, online)

        if negative_file: # (random) reliably negative examples
            neg_urls = URLUtility.load_urls(negative_file)
            neg_urls = neg_urls[:200]
        else:
            neg_urls = []
        print "neg_urls: ", len(neg_urls)
        neg_sites = self.fetcher.fetch_sites(neg_urls, 1, None, online)
        ranker = Ranker(train_sites, representation, ranking, neg_sites)

        # Data
        scores = [] # Avoid exception when iters=0
        #seed_sites = self.train_urls # topk urls from each search batch
        seed_sites = train_sites # topk urls from each search batch
        selected_urls = set() # avoid searching with these urls again
        results = [] # Search results for ranking 
        urls = set() # Avoid fetch and rank these urls again

        # Hyperparameters
        #max_numb_pages = 12000 # stop condition
        max_numb_pages = 51000 # stop condition
        #iters = 500
        iters = 2000

        k = 20 #  number of pages from the newly discovered pages to be added to the seed list
        max_kw = 20 # maximum number of keywords to select from the seed pages
        self.searcher.set_max_keywords(max_kw)

        """
        # Search Strategy
        blsearch = kwsearch = rlsearch = fwsearch = False
        if search == 'bl':
            blsearch = True
            print "Backlink search enable"
        elif search == 'rl':
            rlsearch = True
            print "Related search enable"
        elif search == 'kw':
            kwsearch =  True
            print "Keyword search enable"
        """
        site_mode = False # used in get_top_ranked_urls function 
        if searchop=='rl' or searchop == 'bl':
            site_mode = True
            
        for i in xrange(iters):
            t = time.time()

            print "Searching... ", len(seed_sites), "  seed urls"
            print "\n Iteration ", i, searchop
            new_urls = self.searcher.search(seed_sites, searchop, \
                                            seed_keyword=seed_keyword, \
                                            max_results=max_results)
            new_urls = [url for url in new_urls if url not in urls]
            if len(new_urls)==0:
                print "Searcher found 0 url"
                seed_sites = self.get_top_ranked_urls(scores, k, selected_urls, site_mode)
                if len(seed_sites) == 0:
                    print "Stop. Running out of seeds"
                    break
                else:
                    continue 

            urls.update(new_urls)

            print "Time to search ", i, ": ", time.time()-t
            t = time.time()

            new_sites = self.fetcher.fetch_sites(new_urls, max_pages, selection, online)

            print "Time to fetch ", i, ": ", time.time()-t
            t = time.time()

            print "Size of candidates (before): ", len(results)
            results.extend(new_sites)
            print "Size of candidates (after): ", len(results)
            scores = ranker.rank(results)
            if len(scores)>=max_numb_pages: 
                print "Stop. Retrieved ", max_numb_pages, " pages"
                break
            seed_sites = self.get_top_ranked_urls(scores, k, selected_urls, site_mode)
            if len(seed_sites) == 0:
                print "Stop. Running out of seeds"
                break
            self.save_urls(new_sites, i)
            
            print "Time to rank ", i, ": ", time.time()-t

        self.save_scores(scores)

    def run_mix_search(self, ranking, selection=None, online=True, max_results=50, seed_keyword="gun", search="kw", iters=5, representation='body', negative_file=None):
        """
        seed_sites: urls that are used for search
        selected_urls: urls that were used for search

        Only top-ranked urls will become seed urls

        Important Args:
            ranking: a ranking method
            max_results: Maximum number of results to return in related and keyword search
        """
        max_pages = 1 # Always use single page to represent a website
        train_sites = self.fetcher.fetch_sites(self.train_urls, max_pages, selection, online)

        if negative_file: # (random) reliably negative examples
            neg_urls = URLUtility.load_urls(negative_file)
            neg_urls = neg_urls[:200]
        else:
            neg_urls = []
        print "neg_urls: ", len(neg_urls)
        neg_sites = self.fetcher.fetch_sites(neg_urls, 1, None, online)
        ranker = Ranker(train_sites, representation, ranking, neg_sites)

        # Data
        scores = [] # Avoid exception when iters=0
        #seed_sites = self.train_urls # topk urls from each search batch
        seed_sites = train_sites # topk urls from each search batch
        selected_urls = {} # avoid searching with these urls again
        selected_urls['kw'] = set()
        selected_urls['bl'] = set()
        selected_urls['rl'] = set()
        selected_urls['fw'] = set()
        results = [] # Search results for ranking 
        urls = set() # Avoid fetch and rank these urls again
        sites = set() # used to compute reward 
        

        # Hyperparameters
        #max_numb_pages = 12000 # stop condition
        max_numb_pages = 51000 # stop condition
        #iters = 500
        iters = 2000
        k = 20 #  number of pages from the newly discovered pages to be added to the seed list
        max_kw = 20 # maximum number of keywords to select from the seed pages
        self.searcher.set_max_keywords(max_kw)

        # Initialize Search Operator Selection Strategy
        count = {} # Count number of results yeilded by each search operator
        count['bl'] = count['kw'] = count['rl'] = count['fw'] = 0 
        count['bl'] = 20000 # never choose this
        #ucb = UCB1(['rl', 'bl', 'kw'])
        ucb = UCB1(['rl', 'bl', 'kw', 'fw'])
        
        site_mode = False # used in get_top_ranked_urls function 

        for i in xrange(iters):
            t = time.time()

            print "Searching... ", len(seed_sites), "  seed urls"
            searchop = self.select_searchop(count, search, ucb)

            if searchop=='rl' or searchop=='bl':
                site_mode = True
            else:
                site_mode = False

            print "\n Iteration ", i, searchop 
            new_urls = self.searcher.search(seed_sites, \
                                            searchop, seed_keyword=seed_keyword, \
                                            max_results=max_results)
            new_urls = [url for url in new_urls if url not in urls]

            if len(new_urls)==0:
                print "Searcher found 0 url"
                seed_sites = self.get_top_ranked_urls(scores, k, selected_urls[searchop], site_mode) # Backlink search and related search only use host name to form the query. searchop!='kw' <-> searchop=='bl' or searchop=='rl'
                if len(seed_sites) == 0:
                    print "Stop. Running out of seeds"
                    break
                else:
                    continue 

            urls.update(new_urls)

            print "Time to search ", i, ": ", time.time()-t
            t = time.time()

            new_sites = self.fetcher.fetch_sites(new_urls, max_pages, selection, online)

            print "Time to fetch ", i, ": ", time.time()-t
            t = time.time()

            temp = len(results)
            results.extend(new_sites)
            print "Size of candidates (after): ", len(results)
            print "Number of new candidates (after): ", len(results) - temp
            scores = ranker.rank(results)
            if len(scores)>=max_numb_pages: 
                print "Stop. Retrieved ", max_numb_pages, " pages"
                break
            #seed_sites = self.get_top_ranked_urls(scores, k, selected_urls[searchop])
            seed_sites = self.get_top_ranked_urls(scores, k, selected_urls[searchop], site_mode) # Backlink search and related search only use host name to form the query. searchop!='kw' <-> searchop=='bl' or searchop=='rl'
            if len(seed_sites) == 0:
                print "Stop. Running out of seeds"
                break
            self.save_urls(new_sites, i)
            
            # Update information from the search results to the operation selector
            count[searchop] += len(new_urls)
            if (search == 'bandit') and new_sites:
                reward = self.get_reward(scores, new_sites, sites)
                print "UCB Rewards", searchop, reward
                ucb.update(searchop, reward, len(new_sites))
                sites.update([s.get_host() for s in new_sites])
            print "Time to rank ", i, ": ", time.time()-t

        self.save_scores(scores)

    def get_reward(self, ranklist, new_sites, prev_sites):
        """
        Compute the reward based on the positions of sites in the ranklist
        reward = len(ranklist) * len(sites) / sum(positions of sites)

        Parameters:
            - ranklist: list of all the discovered sites and their scores
            - new_sites: list of sites discovered by the current search operator
            - prev_sites: list of discovered sites

        """
        # Construct mapping between url and its position in the ranklist
        url2pos = {}
        for i, item in enumerate(ranklist):
            site, score = item
            url2pos[site.get_url()] = i

        #pos = [url2pos[url] for url in new_sites if url in url2pos]
        #pos = [url2pos[url] for url in new_sites if url in url2pos and URLUtility.get_host(url) not in prev_sites]
        pos = []
        for site in new_sites:
            url = site.get_url()
            host = site.get_host()
            if (url in url2pos) and (host not in prev_sites):
                pos.append(url2pos[url])
        if len(pos)==0:
            return 0
        #reward = 1 - sum(pos)/(float(len(ranklist)*len(pos))) # y = 1 - x, where x = pos/n
        #reward = self.compute_curved_reward(pos, len(ranklist))
        reward = self.compute_site_favored_reward(pos, len(ranklist), len(new_sites))
        return reward

    def compute_site_favored_reward(self, pos, n, k):
        """
        sum(1 - pos/n) / k
        """
        reward = (len(pos) - sum(pos)/float(n))/k # y = 1 - x, where x = pos/n
        return reward

    def compute_curved_reward(self, pos, n):
        """
        y = sqrt(1-x^2)
        where x = pos/n
        """
        reward = 0
        nsq = float(n*n)
        for p in pos:
            reward += math.sqrt(1 - p*p/nsq)
        return reward/float(len(pos))
    
    def select_searchop(self, count, search, ucb):
        if search == 'mix':
            op =  min(count, key=count.get)
        elif search == 'bandit':
            op = ucb.select_arm()
            print "Bandit selects ", op
        else:
            print "Wrong search strategy", search
            sys.exit(0)
        return op 

def make_name(args):
    """
    Create name for output file
    - Names are distinct from different runs
    - Names are descriptive
    """
    domain = args.seedfile.split('/')[-2]
    name = 'result_' + domain + '_' + args.rank + '_search-' + str(args.search) + '_count-' + str(args.count) + '_' + str(time.time()) + '.csv'
    return name

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-seed", "--seedfile", help="path to seed file", type=str)
    parser.add_argument("-cand", "--candfile", help="path to candidate file", type=str)
    parser.add_argument("-out", "--datadir", help="path to output directory", type=str)
    parser.add_argument("-rank", "--rank", help="ranking method, choose between (all, pu_learning, jaccard, cosine, bayesian_bin, bayesian_tfidf, oneclass, random)", type=str)
    parser.add_argument("-re", "--representation", help="website representation, choose between (body, meta)", type=str)
    parser.add_argument("-se", "--selection", help="method to select representative pages in a website, choose between (random, search). Default is None", type=str)
    parser.add_argument("-mc", "--maxcand", help="Maximal number of candidates", type=int)
    parser.add_argument("-mp", "--maxpages", help="Maximal number of pages selected in a website, excluded the homepage", type=int)
    parser.add_argument("-count", "--count", help="Maximal number of results to return in search operators", type=int)
    parser.add_argument("-skw", "--seedkeyword", help="keyword used to create queries in keyword search", type=str)
    parser.add_argument("-o", "--online", action='store_true') # default = False
    parser.add_argument("-i", "--iteration", help="Number of iterations", type=int)
    parser.add_argument("-neg", "--negfile", help="path to file with dmoz urls considered as negatives", type=str)
    parser.add_argument("-search", "--search", help="search strategy: bl, kw, rl, fw, bandit, mix", type=str)

    args = parser.parse_args()
    parser.print_help()
    if not args.seedkeyword:
        args.seedkeyword = 'gun'
        print "Missing seed keyword"

    result_file = args.datadir + "/" + make_name(args) 
    sd = SiteDiscovery(args.seedfile, result_file, args.datadir)
    if args.search=='mix' or args.search=='bandit':
        sd.run_mix_search(args.rank, args.selection, args.online, args.count, args.seedkeyword, args.search, args.iteration, args.representation, args.negfile)
    else:
        sd.run(args.rank, args.selection, args.online, args.count, args.seedkeyword, args.search, args.iteration, args.representation, args.negfile)

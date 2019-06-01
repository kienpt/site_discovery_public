import sys
import copy
import time
import argparse
from urlparse import urlparse
from url_normalize import url_normalize

sys.path.append("utils")
sys.path.append("ranking")
from ranker import Ranker
from urlutility import URLUtility
from multiproc_fetcher import Fetcher

def evaluate_recall(result_file, test_file):
    """ Count number of urls in test found"""
    test_host = set()
    with open(test_file) as lines:
        for line in lines:
            url = line.strip()
            #url = url_normalize(url)
            host = URLUtility.get_tld(url)
            test_host.add(host)  

    found_host = set()
    with open(result_file) as lines:
        for line in lines:
            values = line.strip().split()
            url = values[1]
            #url = url_normalize(url)
            host = URLUtility.get_tld(url)
            found_host.add(host)

    found = 0
    for host in found_host:
        if host in test_host:
            found += 1
            print host, found

    print found, len(test_host)

def get_seednumbs(min, max, step):
    seednumbs = []
    for i in xrange(max, min-1, -step):
        seednumbs.append(i)
    return seednumbs

def evaluate_ranking(seed_file, candidate_file, negative_file, data_dir, rankings, max_cand, representation, test_ratio, online, selection=None, max_pages=1, prf=False, seednumbs=None):
    """
    test_ratio: percentage of test urls splitted from seed urls
    """
    t = time.time()
    seed_urls = URLUtility.load_urls(seed_file)
    cand_urls = URLUtility.load_urls(candidate_file)
    neg_urls = URLUtility.load_urls(negative_file)

    # Split train and test urls
    split = int((1-test_ratio)*len(seed_urls))
    test_urls = seed_urls[split:]
    train_urls = seed_urls[:split]

    # Fetch the train, test and candidate sites 
    print "Loading the cache"
    fetcher = Fetcher(data_dir)
    if selection == "mix":
        # This is to prove the yet ineffectiveness of multipages representation
        train_selection = test_selection = "search"
        cand_selection = "random"
    else:
        train_selection = test_selection = cand_selection = selection

    print "\nFetching train sites"
    train_sites = fetcher.fetch_sites(train_urls, max_pages, train_selection, online)

    print "Time to fetch train sites: ", time.time()-t
    t = time.time()

    if seednumbs:
        seednumbs = get_seednumbs(seednumbs[0], len(train_sites), seednumbs[1])
    else:
        seednumbs = [len(train_sites)]
    print "seednumbs", seednumbs
    for seednumb in seednumbs:
        train_sites = train_sites[:seednumb+1]
        #for s in train_sites:
        #    for p in s:
        #        print p.get_url()
        print "\nFetching cand sites"
        cand_sites = fetcher.fetch_sites(cand_urls, max_pages, cand_selection, online)
        print "\nFetching test sites"
        test_sites = fetcher.fetch_sites(test_urls, max_pages, test_selection, online)
        print "\nFetching negative sites"
        neg_sites = fetcher.fetch_sites(neg_urls, 1, None, online)
        print "Time to fetch cand, test, neg sites: ", time.time()-t

        cand_sites = cand_sites[:max_cand]
        max_cand -= len(test_sites)
        cand_sites.extend(test_sites)
        print "Number of seed sites: ", len(train_sites)
        print "Number of test sites: ", len(test_sites)
        print "Number of candidate sites: ", len(cand_sites)
        print "Ranking methods: ", rankings
        if online:
            print "Running online mode"
        else: print "Running offline mode"

        # Initialize the ranking models
        for ranking in rankings:
            # Train
            print "Ranking..."
            t = time.time()
            ranker = Ranker(copy.deepcopy(train_sites), representation, ranking, neg_sites) # train_sites might be changed in the object initialization 
            print "Time to initialize ranker: ", time.time()-t
            t = time.time()
            top_sites = ranker.rank(cand_sites, prf)
            print "Time to rank: ", time.time()-t

            # Evaluate
            print "Evaluating ranking results"
            site2rank = {}
            site2website = {}
            for i, site_score in enumerate(top_sites):
                site = site_score[0].get_host()
                if site not in site2rank:
                    site2rank[site] = i
                    site2website[site] = site_score[0]
            test_scores = [] 
            #test_count = 0
            for url in test_urls:
                site = URLUtility.get_host(url)
                if site in site2rank:
                    #test_count += 1
                    print site, site2rank[site]
                    print [p.get_url() for p in site2website[site]]
                    test_scores.append(site2rank[site])
            test_scores = sorted(test_scores)
            mean = sum(test_scores)/float(len(test_scores))
            mean = round(mean, 2)
            median = test_scores[(len(test_scores)-1)/2]
            #prec_at_k = round(len([s for s in test_scores if s<=len(test_urls)])/float(test_count), 4)*100
            prec_at_k = round(len([s for s in test_scores if s<len(test_scores)])/float(len(test_scores)), 4)*100
            precs = compute_prec(test_scores)
            print "RESULTS_SEEDNUMB", len(train_sites)
            print "RESULTS_RAW," + ranking + ',' + ','.join([str(s) for s in test_scores])
            print "RESULTS_AGGREGATION," + ranking + ',' + str(mean) + ','  + str(median) + ',' + str(prec_at_k)
            print "RESULTS_PRECS", ranking + ',' + ','.join([str(p) for p in precs])

            # Debug: print top 10 urls
            print "Top 10 urls: "
            for item in top_sites[:20]:
                print item[0].get_host(), item[1]
                print [p.get_url() for p in item[0]]

            # Clear the pre-computed vectorization from previous runs
            clear(train_sites)
            clear(cand_sites)
            clear(test_sites)
            clear(neg_sites)

def compute_prec(scores):
    """
    Compute the precision at k, where k is in the range of [1,max_k]
    """
    precs = []
    max_k = len(scores)
    for k in xrange(max_k):
        prec_at_k = round(len([s for s in scores if s<=k])/float(k+1), 4)*100
        precs.append(prec_at_k)
    return precs

def clear(sites):   
    for s in sites:
        s.clear()


def print_arguments(args):
    print "Pseudo-Relevance Feedback: ", args.prf

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-seed", "--seedfile", help="path to seed file", type=str)
    parser.add_argument("-cand", "--candfile", help="path to candidate file", type=str)
    parser.add_argument("-neg", "--negfile", help="path to file with dmoz urls considered as negatives", type=str)
    parser.add_argument("-out", "--datadir", help="path to output directory", type=str)
    parser.add_argument("-rank", "--rank", help="ranking method, choose between (all, pu_learning, jaccard, cosine, bayesian_bin, bayesian_tfidf, oneclass, random)", type=str)
    parser.add_argument("-re", "--representation", help="website representation, choose between (body, meta)", type=str)
    parser.add_argument("-se", "--selection", help="method to select representative pages in a website, choose between (random, search, mix). Default is None", type=str)
    parser.add_argument("-mc", "--maxcand", help="Maximal number of candidates", type=int)
    parser.add_argument("-mp", "--maxpages", help="Maximal number of pages selected in a website, excluded the homepage", type=int)
    parser.add_argument("-o", "--online", action='store_true') # default = False
    parser.add_argument("-prf", "--prf", help="Pseudo-relevance feedback", action='store_true') # default = False
    parser.add_argument("-sn", "--seednumbs", help="[min,step] parameters to generate different number of seeds. ", nargs=2, type=int) 
    args = parser.parse_args()

    #all_rankings = ["pu_learning", "jaccard", "cosine", "bayesian_bin", "bayesian_tfidf", "oneclass", "random"]
    all_rankings = ["pu_learning", "jaccard", "cosine", "bayesian_bin", "bayesian_tfidf", "oneclass", "classifier", "stacking", "stacking_rrf"]
    if args.rank == "all":
        rank = all_rankings 
    elif args.rank in all_rankings:
        rank = [args.rank]
    else:
        print "Wrong ranking argument"
        sys.exit()

    print_arguments(args)

    maxcand = args.maxcand if args.maxcand else sys.maxint
    maxpages = args.maxpages if args.maxpages else 1

    evaluate_ranking(args.seedfile, args.candfile, args.negfile, args.datadir, rank, maxcand, representation=args.representation, test_ratio=0.5, online=args.online, selection=args.selection, max_pages=maxpages, prf=args.prf, seednumbs=args.seednumbs)

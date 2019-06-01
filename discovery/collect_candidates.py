"""
Use search operators to retrieve candidate websites for each domain.
Two main actions:
    - Fetch seed websites. Use backward, forward and related search to acquire candidate websites
    - Extract high TF-IDF keywords from the seed websites. Use keyword search to acquire candidate websites 

Input:
------
Seed websites

Output:
------
Candidate websites
"""
import sys
sys.path.append("search_apis")
sys.path.append("utils")
from urlutility import URLUtility
from multiproc_fetcher import Fetcher
from search_apis import Search_APIs
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import heapq

def collect_candidates(seed_urls, data_dir):
    fetcher = Fetcher(data_dir) 
    print seed_urls
    seed_sites = fetcher.fetch_sites(seed_urls)
    searcher = Search_APIs(data_dir, fetcher)

    candidates = set()
    print "Running related search and backward-forward search"
    for seed in seed_sites:
        # Run related search
        urls = searcher.search_related(seed.get_host())
        candidates.update(urls)

        # Run backward search
        urls = searcher.search_backward_forward(seed.get_host())
        candidates.update(urls)

    # Run keyword search
    print "Running keyword search"
    keywords = extract_keywords(seed_sites)
    for keyword in keywords:
        candidates.update(searcher.search_keywords(keyword))

    output_file = make_output_filename(data_dir, seed_file)
    save(candidates, output_file)

def save(urls, output_file):
    f = open(output_file, "a")
    for url in urls:
        f.write(url + "\n")
    f.close()

def extract_keywords(sites, k=10):
    """
    Extract top k most frequent keywords
    """
    stop = stopwords.words('english')
    counter = Counter()
    for site in sites:
        for p in site:
            text = p.get_text('meta')
            text = URLUtility.clean_text(text) 
            words = word_tokenize(text)
            words = [word for word in words if word not in stop and len(word)>2]
            counter += Counter(words)
    
    # Get the topk words
    counter = [(counter[w], w) for w in counter if counter[w]>1] # convert to array
    heapq.heapify(counter)
    topk = heapq.nlargest(k, counter)
    print "Top extracted keywords: ", topk
    return [w[1] for w in topk]

def make_output_filename(data_dir, seed_file):
    seed_filename = seed_file.split("/")[-1].split(".")[0]
    return data_dir + "/" + seed_filename + "_candidates.txt"
                    
if __name__=="__main__":
    seed_file = sys.argv[1]
    data_dir = sys.argv[2]
    seed_urls = URLUtility.load_urls(seed_file)
    collect_candidates(seed_urls, data_dir)

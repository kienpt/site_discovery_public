"""
#if ".cat" in host or ".es" in host or ".ru" in host or ".ua" in host or ".cz" in host or ".tr" in host or ".de" in host or ".vn" in host or ".fr" in host or ".bg" in host or ".nl" in host or ".be" in host or ".uz" in host or ".eu" in host or ".cn" in host or ".jp" in host or ".pl" in host or ".ro" in host or ".bt" in host or ".br" in host or ".fi" in host or ".se" in host or ".tw" in host or ".dk" in host or ".cl" in host or ".at" in host or ".ch" in host or ".it" in host or ".il" in host or ".ly" in host or ".wikipedia" in host or ".li" in host or ".id" in host:
"""
import sys
sys.path.append("../../../../utils")
from urlutility import URLUtility
from urlparse import urlparse
from collections import defaultdict
from random import shuffle
import traceback

def filter_duplicate_sites():
    """
    Read urls from infile and output one url for each site
    """
    infile = sys.argv[1]
    outfile = sys.argv[2]
    out = open(outfile, "w")
    
    sites = set()
    with open(infile) as lines:
        for line in lines:
            url = line.strip()
            s = URLUtility.get_host(url)
            if s not in sites:
                out.write(s + "\n")
                sites.add(s)
    out.close()

def get_unused_urls():
    """
    Skip urls associated with the stopwords
    """
    k = 2000 # get 2000 urls
    used_urls_file = sys.argv[1] 
    new_urls_file = sys.argv[2]
    outfile = sys.argv[3]
    out = open(outfile, "w")
    
    used_urls = URLUtility.load_urls(used_urls_file)
    used_sites = set([URLUtility.get_host(url) for url in used_urls])

    stopwords = ['gun', 'weapon', 'firearm']
    sites = set()
    with open(new_urls_file) as lines:
        for line in lines:
            try:
                skip = False
                for w in stopwords:
                    if w in line:
                        skip = True
                if skip: continue

                label, host, url, topic = line.strip().split()
                if host in used_sites:
                    continue
                sites.add(host) 
            except:
                traceback.print_exc()
    sites = list(sites)
    indices = [i for i in xrange(len(sites))]
    shuffle(indices)
    indices = indices[:k]
    for i in indices:
        out.write(sites[i] + "\n")
    out.close()

get_unused_urls()

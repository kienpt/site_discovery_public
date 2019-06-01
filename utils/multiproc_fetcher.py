import re
import os
import sys
import json
import time
import pickle
import random
import requests
import traceback
import url_normalize
from multiprocessing import Pool
from multiprocessing import Queue
from multiprocessing import Process
# Disable insecure warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) 

#from requests.adapters import TimeoutSauce

#class MyTimeout(TimeoutSauce):
#    def __init__(self, *args, **kwargs):
#        connect = kwargs.get('connect', 5)
#        read = kwargs.get('read', connect)
#        super(MyTimeout, self).__init__(connect=connect, read=read)
#
#requests.adapters.TimeoutSauce = MyTimeout

sys.path.append("utils")
sys.path.append("extraction")
sys.path.append("search_apis")


from page import Page
from cache import Cache
from website import Website
from urlutility import URLUtility
from bing_search import Bing_Search
from link_extractor import Link_Extractor


def init_cache(filename):
    print "Loading ", filename
    return Cache(filename)

class Fetcher:
    def __init__(self, data_dir, data_file=None, caching=True):
        """
        Args:
            caching: if False, do not store the data. 
                   In this case, fetch() might be called for the same urls more than one time.
                   So, url deduplication needs to be handled outside the class
        """
        if caching:
            print "caching is TRUE - Save the fetched pages"
        else:
            print "caching is False - Don't save the fetched pages"

        self.link_extractor = Link_Extractor()
        self.header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'}
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)      

        self.max_html_size = 1000000 # discard exceptionally large files
        self.proc_numb = 32 # number of processes
        self.timeout = 5 # requests timeout
        self.caching = caching
        self.uniq_urls = set() # Avoid re-crawling the previous urls. This variable will keep track of failed urls, which are not stored in discovery class

        """
        # Single process
        self.caches = []
        
        for i in xrange(self.proc_numb):
            name = data_file if data_file else "fetch"
            if i:
                fetch_cache_file = data_dir + "/" + name + "." + str(i) + ".json"
            else:
                fetch_cache_file = data_dir + "/" + name + ".json" # make the file compatible with single process fetcher 
            print fetch_cache_file
            self.caches.append(Cache(fetch_cache_file))
        """
        cache_files = [] # File to store that data
        for i in xrange(self.proc_numb):
            name = data_file if data_file else "fetch"
            if i:
                fetch_cache_file = data_dir + "/" + name + "." + str(i) + ".json"
            else:
                fetch_cache_file = data_dir + "/" + name + ".json" # make the file compatible with single process fetcher 
            cache_files.append(fetch_cache_file)
        pool = Pool(self.proc_numb)
        self.caches = pool.map(init_cache, cache_files)

        bing_api_key = '79be97cfb50b418caf9cd0bff0ece408' #ktp231@nyu.edu
        self.bing_search = Bing_Search(bing_api_key, data_dir)

    def _contains(self, url):
        """ 
        Check the cache if it contains the url.

        Returns:
            return a dict object if url exists in the cache, else return None
        """ 
        for cache in self.caches:
            if cache.contains(url):
                return cache.get(url)
        return None

    def fetch_sites(self, urls, max_pages=1, selection="random", online=True, allow_fetch_later=False):
        """
        Fetch the sites.
        Step 1: Fetch the home pages
        Step 2: Select representative pages from the fetched sites
        Step 3: Fetch the selected representative pages
        Step 4: Merge the fetched results 

        Parameters:
        -----------
        urls: list of url. Each url represents a website
        max_pages: maximum number of pages to be selected in each website
        selection: method to select pages in a website
        online (boolean): online or offline mode. In offline mode, read data from the cache.

        Returns:
        --------
        list<website>: list of fetched websites
        """
        """
        # Hack: used pre-fetched data
        if online==False and selection=="search":
            # Read from the cache and return results
            print "hacking ..."
            print max_pages
            websites = {}
            for url in urls:
                tld = URLUtility.get_tld(url)
                websites[tld] = Website(url)
            for url in self.cache.keys():
                tld = URLUtility.get_tld(url)
                if tld in websites:
                    #if len(websites[tld].pages)<max_pages:
                    page = Page(url)
                    page.load_from_json(self.cache.get(url))
                    websites[tld].add_page(page)

            websites = [w for w in websites.values() if not w.is_empty()]
            print "Number of websites that found in cache: ", len(websites)
            for w in websites:
                print w.get_host(), len(w.pages)

            return websites
        """

        #THE BELOW CODE WORKS FOR MULTIPLE-PAGES CASE BUT NOT OPTIMIZED FOR ONE-PAGE CASE
        # Step 1: Fetch the home pages
        pages = self.fetch_pages(urls, online, allow_fetch_later) 
        max_pages -= 1 # exclude the home page
        websites = {}
        for p in pages:
            tld = p.get_tld()
            w = Website(p.get_url())  
            w.add_page(p)
            websites[tld] = w
       
        # Step 2: Select representative pages from the fetched sites
        if max_pages:
            print "    Selecting insite pages for representation. Selection method: ", selection
            insite_urls = []
            if selection==None:
                # Only fetch the homepage
                return websites.values()
            if selection=="random":
                for page in pages:
                    insite_urls.extend(self._select_random(page, max_pages))
            elif selection=="search":
                for page in pages:
                    insite_urls.extend(self._select_by_search(page, max_pages))
            else:
                print "Wrong selection method"

            print "    Selected ", len(insite_urls), " urls from ", len(pages), " sites"

            # Step 3: Fetch the selected representative pages
            pages = self.fetch_pages(insite_urls, online, allow_fetch_later)

            # Step 4: Merge the fetched results 
            for p in pages:
                tld = p.get_tld()
                if tld not in websites:
                    print "    Error: host does not exist", tld, p.get_url()
                else:
                    websites[tld].add_page(p)

        total_pages = sum([len(websites[tld].pages) for tld in websites])
        print total_pages, len(websites)
        if websites:
            print "    Average number of pages per site: ", total_pages/float(len(websites))

        return websites.values()
        """
        # Keep one url for each website
        uniq_hosts = set()
        temp_urls = []
        for url in urls:
            host = URLUtility.get_host(url)
            if host not in uniq_hosts:
                uniq_hosts.add(host)
                temp_urls.append(url)
                print "Fetching ", url
        urls = temp_urls

        # Fetch
        pages = self.fetch_pages(urls, online, allow_fetch_later) 

        # Construct website list from page list (one page per site)
        websites = []
        for p in pages:
            w = Website(p.get_url())
            w.add_page(p)
            websites.append(w)
        return websites
        """

    def _select_random(self, page, max_pages):
        """
        Select random insite outlinks
        """
        insite_urls = list(set(self.link_extractor.extract_insite_links(page.get_url(), page.get_html())))
        return insite_urls[:max_pages]

        """
        random.seed(len(insite_urls)) # make the randomness reproducible
        #if not insite_urls:
        #    print page.get_url(), len(page.get_html())
        if len(insite_urls)<max_pages:
            return insite_urls
        selected_urls = set()
        while len(selected_urls)<max_pages:
            i = random.randint(0, len(insite_urls)-1)
            selected_urls.add(insite_urls[i])
        return list(selected_urls) 
        """
        random.seed(len(insite_urls)) # make the randomness reproducible

    def _select_by_search(self, page, max_pages):
        """
        Select pages inside a given website using site search

        Args:
            max_pages: maximum number of pages selected in the site
        """
        "Selecing pages using bing search"
        host =  page.get_host()
        keyword = "gun"
        urls = self.bing_search.search_site(keyword, host)
        ret = []
        for url in urls:
            if len(ret)<max_pages:
                if url!=page.get_url():
                    ret.append(url)
        """
        if host=="http://www.armslist.com/":
            print urls
            print ret
            print max_pages
        """
        return ret

    def _load_from_cache(self, urls):
        """
        left_urls = []
        pages = []
        for url in urls:
            obj = self._contains(url)
            if obj:
                page = Page(url)
                page.load_from_json(obj)
                pages.append(page)
            else:
                left_urls.append(url)

        return pages, left_urls
        """
        urls = set(urls)
        loaded_urls = set()
        pages = []
        for cache in self.caches:   
            for url in cache.keys():
                if (url in urls) and (url not in loaded_urls):
                    page = Page(url)
                    loaded_urls.add(url)
                    page.load_from_json(cache.get(url))
                    if page.body: # skip the page whose text extraction was failed
                        pages.append(page)
        left_urls = [url for url in urls if url not in loaded_urls]
        return pages, left_urls

    def fetch_pages(self, urls, online=True, allow_fetch_later=False):
        """
        Fetch the urls that are not in cache

        Parameters:
        -----------
        urls: list of url. Each url represents a website

        Returns:
        --------
        list<website>: list of fetched websites
        """

        # Remove urls that were crawled previously
        print "Number of urls considering to fetch: ", len(urls)
        if allow_fetch_later==False:
            temp_urls = []
            for url in urls:
                if url not in self.uniq_urls:
                    self.uniq_urls.add(url)
                    temp_urls.append(url)
            urls = temp_urls

        print "Number of urls will be fetched: ", len(urls)
        
        pages, urls = self._load_from_cache(urls)
        print "    ", len(pages), " urls loaded from the cache, ", len(urls), " urls left"
        if online:
            jobs = []
            results = Queue()
            for i in range(self.proc_numb):
                p = Process(target = self.fetch_pages_helper, args = (urls, i, self.proc_numb, self.caches[i], results))
                jobs.append(p)

            for p in jobs:
                p.start()

            fetched_pages = [p for _ in jobs for p in results.get()] # Result must be collected before join()

            for p in jobs:
                p.join()

            if urls:
                print "    Fetched ", len(fetched_pages), " urls"
            pages.extend(fetched_pages)

        return pages

    def fetch_pages_helper(self, urls, start, step, cache, results):
        """
        Helper function for parallel fetching 
        """
        max_size = 5000000
        pages = []
      
        for i in range(start, len(urls), step):
            url = urls[i]
            if (i+1)%500==0:
                print "Fetched ", i, " urls"
            page = Page(url)
            try:
                text = ''
                size = 0
                res = requests.get(url, headers=self.header, verify=False, timeout=5, stream=True)
                #t = time.time()
                for chunk in res.iter_content(10000):
                    #if (time.time() - t) > 5:
                    #    break
                    #    raise ValueError('timeout reached')
                    text += chunk
                    size += len(chunk)
                    if size > max_size: 
                        print "Size exceeds ", size
                        raise ValueError('response too large')

                if res.status_code == 200:
                    #page = Page(url)
                    if len(text)<self.max_html_size: 
                        page.add_html(text)
                else:
                    print "Failed to fetch ", url, res.status_code, start
            except:
                print "Failed to fetch ", url
                continue

            # Save to cache. Note that always save the fetched pages even if the requests were failed 
            # since we want to avoid re-fetch these pages in the future
            if self.caching:
                cache.add(url, page.get_json_obj())
            else:
                page.get_json_obj() # hack

            if page.body and (len(page.get_text('body'))>100):
            #if not page.is_empty():
                pages.append(page)
        results.put(pages)

def test():
    fetcher = Fetcher("test/fetcher_test_data")
    urls = URLUtility.load_urls("test/data/urls.txt")
    sites = fetcher.fetch(urls)
    for site in sites:
        for page in site:
            print page.get_text('body')[:100].replace("\n", "")

def _read_urls_from_json(url_file):
    urls = set()
    with open(url_file) as lines:
        for line in lines:
            try:
                jsonobj = json.loads(line)
                for url in jsonobj[1:]:
                    url = URLUtility.normalize(url)
                    urls.add(url)
            except:
                traceback.print_exc()   

    print "Number of urls read from json file: ", len(urls)
    return list(urls)
            
def fetch():
    url_file = sys.argv[1]
    urls = _read_urls_from_json(url_file)
    data_dir = sys.argv[2]
    fetcher = Fetcher(data_dir)
    fetcher.fetch_sites(urls, 3, selection=None, online=True)


if __name__=="__main__":
    #test()
    fetch()

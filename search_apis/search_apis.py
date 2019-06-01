"""
Search APIs 
"""
import sys
import time
import heapq

sys.path.append("utils")
sys.path.append("extraction")
from cache import Cache
from moz import Moz_Search
from fetcher import Fetcher
from collections import Counter
from urlutility import URLUtility
from bing_search import Bing_Search
from google_search import Google_Search
from link_extractor import Link_Extractor

import nltk
from nltk.corpus import stopwords
from url_normalize import url_normalize


class Search_APIs(object):
    def __init__(self, data_dir, fetcher):
        google_api_key = ""
        if not google_api_key:
            print "Error! google_api_key is missing"
            sys.exit(1)
        google_cse_id = "" # Google custome search engine id
        if not google_cse_id:
            print "Error! google_cse_id is missing"
            sys.exit(1)

        self.google = Google_Search(google_api_key, google_cse_id)
        self.google_delay = 1 # 5QPS limit: https://developers.google.com/webmaster-tools/search-console-api-original/v3/limits

        bing_api_key = ""
        if not bing_api_key:
            print "Error! bing_api_key is missing"
            sys.exit(1)
        self.bing = Bing_Search(bing_api_key)
        self.bing_delay = 1

        # Setting cache for related search
        related_cache_file = data_dir + "/related_search.json"
        self.related_cache = Cache(related_cache_file)
        print "Loaded ", self.related_cache.length(), " queries from related search cache"

        # Setting cache for backlink search
        access_id = ""
        if not access_id:
            print "Error! access_id is missing"
            sys.exit(1)
        secret_key = ""
        if not secret_key:
            print "Error! secret_key is missing"
            sys.exit(1)
        self.moz = Moz_Search(access_id, secret_key)
        backlink_cache_file = data_dir + "/backlink_search.json"
        self.backlink_cache = Cache(backlink_cache_file)
        print "Loaded ", self.backlink_cache.length(), " queries from backlink search cache"
        self.moz_delay = 1

        # Setting cache for keyword search
        keyword_cache_file = data_dir + "/keyword_search.json"
        self.keyword_cache = Cache(keyword_cache_file)
        print "Loaded ", self.keyword_cache.length(), " queries from keyword search cache"

        # Setting cache for forward search
        #self.fetcher = Fetcher(data_dir, "/forward_search.json")
        self.fetcher = fetcher
        self.link_extractor = Link_Extractor()

        self.k = 10 # Number of keywords selected in each extraction
        self.max_urls = 10 # maximum number of urls to extract from each pages
        self.keywords = set() # Keywords extracted from relevant sites

    def set_max_keywords(self, max_kw):
        self.k = max_kw

    def _extract_keywords(self, sites, k=10):
        """
        Extract top k most frequent keywords. Skip ones that were selected.
        """
        stop = stopwords.words('english')
        counter = Counter()
        for site in sites:
            for p in site:
                text = p.get_text('meta')
                text = URLUtility.clean_text(text) 
                words = nltk.word_tokenize(text)
                words = [word for word in words if word not in stop and len(word)>2]
                bigram_words = [words[i] + ' ' + words[i+1] for i in xrange(len(words)-1)]
                counter += Counter(words + bigram_words)
        
        # Get the topk words
        """
        counter = [(counter[w], w) for w in counter if counter[w]>1] # convert to array
        heapq.heapify(counter)
        topk = heapq.nlargest(k, counter)
        return [w[1] for w in topk]
        """
        top_words = counter.most_common(k + len(self.keywords)) 
        result = [] # list of keywords to return
        i = 0
        while len(result)<k and i<len(top_words):
            if top_words[i][0] not in self.keywords:
                result.append(top_words[i][0])
                self.keywords.add(top_words[i][0])
            i += 1
        print "    List of selected keywords: ", result
        return result

    def search(self, sites, searchop, seed_keyword="", max_results=50):
        """
        Args:
            max_results: Maximum number of results to return in Bing/Google search
            search: str - potential values: 'rl', 'kw', 'fw', 'bl'
        """
        #sites = self.fetcher.fetch_sites(urls)

        results = set()
        if searchop == 'rl':
            for w in sites:
                print "    Running related search..."
                urls = self.search_related(w.get_host(), max_results)
                results.update(urls)

        elif searchop == 'bl':
            """
            for w in sites:
                print "    Search backlinks..."
                urls = self.search_backward_forward(w.get_host())
                results.update(urls)
            """
            urls = self.search_backward_forward_batch(sites)
            results.update(urls)

        elif searchop == 'fw':
            #urls = [w.get_url() for w in sites]
            print "    Forward search...", len(sites), " urls"
            urls = self.search_forward_sites(sites)
            results.update(urls)

        # Run keyword search
        elif searchop == 'kw':
            print "    Searching by keyword"
            keywords = self._extract_keywords(sites, self.k)
            for keyword in keywords:
                if seed_keyword:
                    keyword = seed_keyword + ' ' + keyword
                urls = self.search_keywords(keyword, max_results, se='bing')
                results.update(urls)


        print "    Found ", len(results), " urls"
        return results

    def search_backward_forward(self, url):
        """
        Search related pages using backlink search and forward search

        Returns:
            - list of urls (potentially duplicated)
        """
        t = time.time()
        backlinks = self.search_backward(url)
        print "Backlink search time: ", time.time() - t
        t = time.time()
        fwlinks =  self.search_forward(backlinks)
        print "Forward search time: ", time.time() - t
        return backlinks + fwlinks

    def search_backward_forward_batch(self, sites):
        """
        Search related pages using backlink search and forward search

        Parameters:
            - sites: list of Website objects
        Returns:
            - list of urls (potentially duplicated)
        """
        t = time.time()
        backlinks = set()
        for site in sites:
            backlinks.update(self.search_backward(site.get_host()))
        backlinks = list(backlinks)
        print "Backlink search time: ", time.time() - t

        t = time.time()
        fwlinks =  self.search_forward(backlinks)
        print "Forward search time: ", time.time() - t
        return backlinks + fwlinks

    def search_backward(self, url):
        """
        Search backlinks using MOZ APIs

        Returns:
            - list of urls 
        """
        if self.backlink_cache.contains(url):
            results = self.backlink_cache.get(url)
            print "hit backlink query: ", url
        else:
            #time.sleep(self.moz_delay)
            results = self.moz.search_backlinks(url)
            self.backlink_cache.add(url, results) 
    
        print "Backlink Search - Query: ", url, " - Number of results: ", len(results)
        return results

    def search_keywords(self, keyword, max_results, se='google'):
        """
        Search relevant pages by keyword using Google

        Args:
        max_results: maximum number of results to return

        """
        urls = []
        if self.keyword_cache.contains(keyword):
            urls = self.keyword_cache.get(keyword)
            print "hit keyword query: ", keyword
        else:
            if se=='google':
                time.sleep(self.google_delay)
                urls = self.google.search(keyword, max_results)
            else:# default: 'bing'
                time.sleep(self.bing_delay)
                urls = self.bing.search(keyword, max_results)
            self.keyword_cache.add(keyword, urls)

        """
        if 'items' in results:
            for item in results['items']:
                urls.append(url_normalize(item['link']))
        """

        print "Keyword Search - Query: ", keyword, " - Number of results: ", len(urls)
        return urls

    def search_forward_sites(self, sites, insite=False):
        """
        Fetch the pages and extract external links. 
        Args
            - sites: list of Website objects
            - insite: False if extracting links outside the host.
        """
        outlinks = set()
        for site in sites:
            for page in site:
                if insite:
                    links = self.link_extractor.extract_insite_links(page.get_url(), page.get_html())
                else:
                    links = self.link_extractor.extract_external_links(page.get_url(), page.get_html())
                links = self.select_subset(links)
                outlinks.update(links)

        print "Forward Search ", " - Number of results: ", len(outlinks)
        return list(outlinks)
      

    def search_forward(self, urls, insite=False):
        """
        Fetch the pages and extract external links
        Args
            - urls: list of urls
            - insite: False if extracting links outside the host.
        """
        sites = self.fetcher.fetch_sites(urls, allow_fetch_later = True) 
        outlinks = set()
        for site in sites:
            for page in site:
                if insite:
                    links = self.link_extractor.extract_insite_links(page.get_url(), page.get_html())
                else:
                    links = self.link_extractor.extract_external_links(page.get_url(), page.get_html())
                links = self.select_subset(links)
                outlinks.update(links)

        print "Forward Search ", " - Number of results: ", len(outlinks)
        return list(outlinks)

    def select_subset(self, urls):
        """
        Each page might contain thousand of external urls which pollute the results, so we only keep a fixed number of links from each page
        How this works:
            - Pick one url in each site  
            - If not yet reaching max, select random urls
        Returns:
            - list of urls
        """
        if len(urls)<=self.max_urls:
            return urls

        results = []
        """
        cur = urls
        while len(results)<self.max_urls:
            sites = set()
            next = []
            for url in cur: 
                site = URLUtility.get_host(url)
                if site not in sites:
                    sites.add(site)
                    results.append(url)
                else:
                    next.append(url)
                if len(results) == self.max_urls:
                    break
            cur = next
        """
        sites = set()
        for url in urls: 
            site = URLUtility.get_host(url)
            if site not in sites:
                sites.add(site)
                results.append(url)
            if len(results) == self.max_urls:
                break

        return results

    def search_related(self, url, k):
        """
        Return list of related urls using Google related search
        """
        query = "related:" + url
        urls = []
        if self.related_cache.contains(query):
            urls = self.related_cache.get(query)
            print "hit related query: ", query
        else:
            time.sleep(self.google_delay)
            urls = self.google.search(query, k)
            self.related_cache.add(query, urls)

        """
        urls = []
        if 'items' in results:
            for item in results['items']:
                urls.append(url_normalize(item['link']))
        """
 
        print "Related Search - Query: ", url, " - Number of results: ", len(urls)
        return urls

def test():
    # TODO: Use python unitest
    apis = Search_APIs("data_test")
    # print apis.search_keywords("Hello galaxy!")
    url = "http://www.nyu.edu/"
    print apis.search_backward_forward(url)

if __name__=="__main__":
    test()

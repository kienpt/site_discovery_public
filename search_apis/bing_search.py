'''
Reference: https://dev.cognitive.microsoft.com/docs/services/56b43eeccf5ff8098cef3807/operations/56b4447dcf5ff8098cef380d
'''
import httplib, urllib
import traceback
import json
import sys
sys.path.append("utils")
from urlutility import URLUtility
from cache import Cache

class Bing_Search(object):
    def __init__(self, api_key, data_dir=None):
        self.cache = None
        if data_dir:
            cache_file = data_dir + "/bing.json"
            self.cache = Cache(cache_file)
        self.stopext = set([".pdf", ".doc", ".xls"])
        self.headers = {'Ocp-Apim-Subscription-Key': api_key}

    def is_valid(self, url):
        if len(url)<4 or url[-4:] in self.stopext:
            return False
        return True

    def search(self, query_term, count=10):
        """
        Reference: https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-web-api-v5-reference#query-parameters
        Args:
            count: The number of search results to return in the response. If count is greater than 50, paging will be used to fetch the results since maximum results of each query is 50
        """
        if self.cache and self.cache.contains(query_term):
            urls = self.cache.get(query_term)
            return [url for url in urls if self.is_valid(url)]
        urls = []
        offset = 0

        while count>0:
            params = urllib.urlencode({
                # Request parameters
                'q': query_term,
                'count': str(min(count, 50)),
                'offset': str(offset),
                'mkt': 'en-us',
                'safesearch': 'Moderate'})

            try:
                conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
                #conn.request("GET", "/bing/v5.0/search?%s" % params, "{body}", headers)
                conn.request("GET", "/bing/v7.0/search?%s" % params, "{body}", self.headers)
                response = conn.getresponse()
                data = response.read()
                obj = json.loads(data)
                if 'webPages' in obj:
                    webPages = obj['webPages']
                    values = webPages['value']
                    for value in values:
                        if self.is_valid(value['url']):
                            url = URLUtility.normalize(value['url'])
                            if url:
                                urls.append(url)
                conn.close()
            except:
                traceback.print_exc()

            count -= 50
            offset += 1

        if self.cache:
            self.cache.add(query_term, urls)
        return urls

    def search_site(self, keyword, url, k=10):
        """
        Search inside a given website using the search command: "keyword site:url"
        Parameters
            keyword: keyword used to search
            url: top level domain
        Returns 
            list of urls
        """
        keyword = keyword + " site:" + url
        return self.search(keyword, k)

def test_search():
    api_key = ''
    if not api_key:
        print "Error! Bing api_key is missing"
        sys.exit(1)
    bing = Bing_Search(api_key)
    query_term = "gun classified"
    print "Query: ", query_term
    urls = bing.search(query_term, 111)
    for url in urls:
        print url

if __name__=="__main__":
    test_search()

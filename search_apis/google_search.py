import sys
import traceback

sys.path.append("utils")
from urlutility import URLUtility
from googleapiclient.discovery import build


class Google_Search(object):
    def __init__(self, api_key, cse_id):
        self.api_key = api_key
        self.cse_id = cse_id
        self.service = build('customsearch', 'v1', developerKey=api_key)
        self.max_results = 50

    def search(self, keyword, k):
        """
        Search for a keyword and return top matched urls
        Reference: https://developers.google.com/custom-search/json-api/v1/reference/cse/list

        Args:
            k: Number of search results to return. 
        """
        k = min(k, self.max_results) 
        urls = []
        index = 1
        while index<=k:
            try:
                res = self.service.cse().list(q=keyword, cx=self.cse_id, num=10, start=index).execute() # maximum 10 results for each query
                if 'items' in res:
                    res = res['items']
                    for item in res:
                        url = URLUtility.normalize(item['link'])
                        if url:
                            urls.append(url)
                    if len(res)<10:
                        # Early stop paging
                        break
                else:
                    print res
                    break # No more results, stop paging
            except:
                traceback.print_exc()
                break

            index += 10

        return urls

    def search_site(self, keyword, url, k):
        """
        Search inside a given website using the search command: "keyword site:url"
        Return list of urls
        """
        keyword = keyword + " site:" + url
        return self.search(keyword, k)

def test():
    my_api_key = ""
    if not my_api_key:
        print "Error! Google my_api_key is missing"
        sys.exit(1)
    my_cse_id = ""
    if not my_cse_id:
        print "Error! Google my_cse_key is missing"
        sys.exit(1)

    google = Google_Search(my_api_key, my_cse_id)
    query_term = "hello galaxy"
    print "Query: ", query_term
    urls = google.search(query_term, k=10)
    for url in urls:
        print url     

    query_term = "gun"
    site = "https://www.nytimes.com/"
    urls = google.search_site(query_term, site, k=10)
    print "Query: ", query_term, site
    for url in urls:
        print url


if __name__=="__main__":
    test()

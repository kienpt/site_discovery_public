import re
import os
import sys
import json
import requests
import traceback
import url_normalize

sys.path.append("utils")
sys.path.append("extraction")
from page import Page
from urlutility import URLUtility

# Disable insecure warning
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Fetcher:
    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'}
        self.max_html_size = 1000000 # discard exceptionally large files

    def fetch(self, urls, out_file, extraction=True):
        """
        Parameters:
        -----------
        urls: list of url. Each url represents a website

        Returns:
        --------
        list<website>: list of fetched websites
        """
        if os.path.exists(out_file):
            fetched_urls = []
            with open(out_file) as lines:
                for line in lines:
                    try:
                        jsobj = json.loads(line)
                        fetched_urls.append(jsobj['url'])
                    except:
                        traceback.print_exc()
            urls = [url for url in urls if url not in fetched_urls]

        print "Number of urls to fetch: ", len(urls)
        out = open(out_file, 'a+')

        for i, url in enumerate(urls):
            if (i+1)%20==0:
                print "Fetched ", i, " urls"
            try:
                res = requests.get(url, headers=self.header, verify=False, timeout=10)
                if res.status_code == 200:
                    page = Page(url)
                    if len(res.text)<self.max_html_size: 
                        page.add_html(res.text)
                        if extraction:
                            jspage = page.get_json_obj()
                        else:
                            jspage = {'url': url, 'html':res.text}
                        out.write(json.dumps(jspage) + '\n')
                else:
                    print res.status_code, url
            except:
                print "Failed to fetch ", url
                traceback.print_exc()
            
        out.close()

def test():
    fetcher = Fetcher()
    urls = ['http://nyu.edu', 'http://mit.edu']
    out_file = 'test_fetcher.json'
    fetcher.fetch(urls, out_file)

if __name__=="__main__":
    url_file = sys.argv[1]
    out_file = sys.argv[2]
    urls = URLUtility.load_urls(url_file)
    fetcher = Fetcher()
    fetcher.fetch(urls, out_file, True)

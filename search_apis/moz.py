'''
Retrieve backlinks from MOZ
Input:
    input_file: contains list of urls, one a line
Output:
    output_file: contains output from MOZ, in json line format
'''

'''
Install Mozscape:
   git  clone git@github.com:seomoz/SEOmozAPISamples.git 
   python SEOmozAPISamples/python/setup.py install

Monitor usage:
  https://moz.com/products/mozscape/usage

Keys:
  https://moz.com/products/mozscape/access

Limit:
  https://moz.com/products/api/pricing
'''
from mozscape import Mozscape
import sys
import json
import traceback
import time
import pprint
sys.path.append("utils")
from urlutility import URLUtility
from url_normalize import url_normalize

class Moz_Search(object):
    def __init__(self, access_id, secret_key):
        self.client = Mozscape(access_id, secret_key)

    def search_backlinks(self, url, limit=5):
        """
        Return a list of urls
        Args:
            limit: maximum number of results to return
        """
        urls = []
        try:
            results = self.client.links(url, scope="page_to_page", sort="page_authority", filters=["external"], limit=limit)
            #results = self.client.links(url, scope="page_to_page", sort="spam_score", filters=["external"], limit=limit)
            #results = self.client.links(url, scope="page_to_page", sort="page_authority")

            for res in results:
                if 'uu' in res:
                    url = URLUtility.normalize(res['uu'])
                    if url:
                        urls.append(url)
                else:
                    print "Error: key does not exisit"
                    print res
        except:
            traceback.print_exc() 

        return urls

def search_backlinks():
    url_file = sys.argv[1]
    output_file = sys.argv[2]

    access_id = ""
    if not access_id:
        print "Error! moz access_id is missing"
        sys.exit(1)

    secret_key = ""
    if not secret_key:
        print "Error! moz secret_key is missing"
        sys.exit(1)

    moz = Moz_Search(access_id, secret_key)

    out = open(output_file, "w")
    with open(url_file) as lines:
        for line in lines:
            try:
                time.sleep(6)
                values = line.split(",") 
                url = values[0]
                result = moz.search_backlinks(url)
                obj = {}
                obj['url'] = url
                obj['result'] = result
                out.write(json.dumps(obj) + "\n")
            except:
                print "URL:" + url
                traceback.print_exc()
    out.close()

def test_search_backlink():
    access_id = ""
    if not access_id:
        print "Error! moz access_id is missing"
        sys.exit(1)
        
    secret_key = ""
    if not secret_key:
        print "Error! moz secret_key is missing"
        sys.exit(1)

    moz = Moz_Search(access_id, secret_key)
    url = "https://www.infowars.com"
    pprint.pprint(moz.search_backlinks(url))

if __name__=="__main__":
    test_search_backlink()

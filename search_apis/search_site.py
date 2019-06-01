import sys
sys.path.append("utils")
import os
from bing_search import Bing_Search
from google_search import Google_Search
import json
from urlutility import URLUtility

api_key = ""
bing_search = Bing_Search(api_key)

def search_site(url_file, out_file, keyword):
    """
    Write results as json line objects into out_file
    Format of each json object:
        list<str>: list of urls. First url is the main site
    """
    urls = URLUtility.load_urls(url_file)
    site2urls = read_json(out_file)
    k = 10
   
    out = open(out_file, "a+")
    for i, url in enumerate(urls):
        site = URLUtility.get_host(url)
        if site not in site2urls:
            results = bing_search.search_site(keyword, url, 10)
            results = [site, url] + results
            json.dump(results, out)
            out.write("\n")
    out.close()

def read_json(out_file):
    """
    Read the previous search results 
    """
    print "Reading json file ", out_file
    site2urls = {}
    if os.path.exists(out_file):
        with open(out_file) as lines:
            for line in lines:
                try:
                    jsonobj = json.loads(line)
                    site2urls[jsonobj[0]] = jsonobj[1:]
                except:
                    print "Parsing failed. Data: ", line
    print "Total number of sites loaded from the json file: ", len(site2urls)
    return site2urls

def main():
    keyword = "gun"
    url_file = sys.argv[1]
    out_file = sys.argv[2]
    search_site(url_file, out_file, keyword)

if __name__=="__main__":
    main()

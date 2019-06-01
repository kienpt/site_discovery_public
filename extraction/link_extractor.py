import urllib2
import sys
import re
import urlparse
sys.path.append("utils")
from urlutility import URLUtility
import os
import json
import traceback
from bs4 import BeautifulSoup

class Link_Extractor:
    def __init__(self):
        self.LINK_PATTERN = re.compile(r'href="(.*?)"')    
    
    def extract_links(self, url, html):
        '''
        Extract links from html source using regular expression. Return list of links

        Args:
            - url: url of the html source, used to construct absolute url from relative url
            - html: html source
        Returns:
            - links: extracted (normalized and validated) links
        '''
        match = self.LINK_PATTERN.findall(html)
        links = set([])
        for link in match:
            link = urlparse.urljoin(url, link)
            link = URLUtility.validate_link(link)
            if link:
                link = URLUtility.normalize(link)
                if link:
                    links.add(link)
        return list(links)

    def extract_links_bs(self, url, html):
        '''
        Extract all outlinks from html using beautiful soup. Return list of links

        Args:
            - url: url of the html source, used to construct absolute url from relative url
            - html: html source
        Returns:
            - links: list of outlinks
       
        '''
        try:
            soup = BeautifulSoup(html, 'lxml')
        except:
            print "Parsing with beautiful soup failed"
            return []
        links = set()
        for tag in soup.findAll('a', href=True):
            link = tag['href']
            try:
                link = urlparse.urljoin(url, link)
            except:
                continue
            link = URLUtility.validate_link(link)
            if link:
                link = URLUtility.normalize(link)
                if link:
                    links.add(link)
        return list(links)

    def extract_external_links(self, url, html):
        '''
        Extract external outlinks, that link to different websites
        Returns: 
            - list of unique urls
        '''
        try:
            soup = BeautifulSoup(html, 'lxml')
            links = set()
            tld = URLUtility.get_tld(url)

            for tag in soup.findAll('a', href=True):
                link = tag['href']
                values = urlparse.urlparse(link)
                if (values.netloc=="") or (values.netloc==tld) or (tld in values.netloc):
                    continue
                link = URLUtility.validate_link(link)
                if link:
                    link = URLUtility.normalize(link)
                    if link:
                        links.add(link)
            return list(links)
        except:
            traceback.print_exc()
            return []

    def extract_insite_links(self, url, html):
        '''
        Returns: 
            - list of insite urls that are different from the input url
        '''
        try:
            soup = BeautifulSoup(html, 'html.parser')
            #soup = BeautifulSoup(html, 'lxml') # Couldn't parse http://www.gunsinternational.com/
            links = set()
            tld = URLUtility.get_tld(url)
            for tag in soup.findAll('a', href=True):
                link = tag['href']
                try:
                    link = urlparse.urljoin(url, link)
                except:
                    traceback.print_exc()
                    continue
                values = urlparse.urlparse(link)
                if tld in values.netloc:
                    link = URLUtility.validate_link(link)
                    if link:
                        link = URLUtility.normalize(link)
                        if link and link!=url:
                            links.add(link)
            return list(links)
        except:
            print "Parsing with BeautifulSoup failed"
            return []
def test():
    import requests
    url = "https://en.wikipedia.org/wiki/Elon_Musk"
    url = "http://www.nyu.edu/"
    url = "http://www.gunsinternational.com/"
    link_extractor = Link_Extractor()
    res = requests.get(url)
    if res.status_code == 200:
        html = res.text.strip()
        #print html.encode('utf-8')
        links = link_extractor.extract_insite_links(url, html)
        #links = link_extractor.extract_external_links(url, html)
        for link in links:
            print link
    else:
        print res.status_code

if __name__=="__main__":
    test()

import urllib2
from urlparse import urlparse
from urlparse import urldefrag
import  url_normalize
import re
import traceback
import tldextract


class URLUtility:
    END_PATTERN = re.compile('.*?\.(pdf|jpg|png|mp4|mp3|wmv|css|ico|xml|txt|json|svg)$')
    FILTER_PATTERN = re.compile('\.(css|xml)')
    WORD_NUMB_PATTERN = re.compile('[\W_]+')

    @staticmethod
    def validate_link(link):
        '''
        - Filter css, js, media files (pdf, jpg, png, etc.)
        - Validate the link

        Returns: 
            - None if link should be filtered or invalid.
        '''
        try:        
            link = link.lower()

            #Remove link that does not point to html page 
            match = URLUtility.FILTER_PATTERN.search(link)
            if match != None:
                return None
            match = URLUtility.END_PATTERN.search(link)
            if match != None:
                return None

            #Remove link that does not start with http, i.e mailto:
            if not link.startswith("http"):
                return None

            return link
        except:
            print "URL can not be validated: " + str(link)
            traceback.print_exc()
            return None

    @staticmethod
    def get_host(url):
        """
        Extract the high level domain from an NORMALIZED url
        """
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain

    @staticmethod
    def get_tld(url):
        values = tldextract.extract(url)
        tld = values.domain + "." + values.suffix
        return tld
 
    @staticmethod
    def normalize(url):
        try:
            url = url.strip().lower()
            url = url.strip("/")
            url =  url_normalize.url_normalize(url)
            if url:
                return urldefrag(url)[0]
            return url
        except:
            traceback.print_exc()
            print "Normalization failed,", url
            return ""

    @staticmethod
    def load_urls(filename, col=0, sep=' '):
        urls = []
        with open(filename) as lines:
            for line in lines:
                url = URLUtility.normalize(line.strip().split(sep)[col])
                urls.append(url)
        return urls

    @staticmethod
    def clean_text(text):
        text = URLUtility.WORD_NUMB_PATTERN.sub(' ', text) # Remove double space, new line, non-word and non-numeric characters
        text = text.strip().lower()
        return text

def test():
    print URLUtility.get_tld("http://austin.backpage.com/SportsEquipForSale/")

if __name__=="__main__":
    test()

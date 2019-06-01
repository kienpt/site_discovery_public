from urlutility import URLUtility
import sys
sys.path.append("extraction")
from text_extractor import Text_Extractor
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from time import time
import numpy as np
import time

class Page(object):
    def __init__(self, url, extraction_type='body', max_size = 1000000):
        """
        Parameters:
        -----------
        text: string
            textual representation of the page. Text can be extracted from the body, title, description, etc.
            This variable is used to cache the result of get_text function

        body: string
            Text extracted from the body part of the html source.
            Body text is usually extracted in fetch process
        
        word_set: set of tokenized words
            It is used to cache the result of get_word_set() function

        vsm: list of real numbers
            vector space model of the extracted text. 
            It is used to cache the result of get_vsm() function
        """
        self.url = url
        self.crawltime = time.time()
        self.html = ''
        self.word_set = set() # Used for jaccard similarity
        self.vsm = None # List of tf-idf values - used for cosine similarity
        self.body = ''
        self.meta = ''
        self.title = ''

        self.max_html_size = max_size # Only accept the html with size les than this to avoid some exceptionally large files

    def clear(self):
        self.vsm = None

    def add_html(self, html):
        self.html = html

    def get_host(self):
        return URLUtility.get_host(self.url)

    def get_tld(self):
        return URLUtility.get_tld(self.url)

    def get_url(self):
        return self.url

    def get_html(self):
        return self.html

    def is_empty(self):
        if not self.html:
            return True
        return False

    def get_crawltime(self):
        return self.crawltime

    """
    def get_text_backup(self, text_type):
        #back up version of get_text
        if not self.html:
            return ''

        if text_type=='body' and self.body:
            return URLUtility.clean_text(self.body)

        if text_type=='body' and not self.text:
            self.body = Text_Extractor.extract_body(self.html).lower()
            self.text = self.body
        elif text_type=='meta' and not self.text:
            self.text = Text_Extractor.extract_metadata(self.html).lower()
        elif text_type=='title' and not self.text:
            self.text = Text_Extractor.extract_title(self.html).lower()

        return URLUtility.clean_text(self.text)
    """

    def get_text(self, text_type):
        """
        Return extracted text from the html. Extract text if neccessary
        NOTE: this function's flow can be confusing cause it does not only serve as extraction
        but also cache the extracted text in different scenarios. 

        Parameters:
        -----------
        text_type: string, optional

        """
        if not self.html:
            return ''

        if text_type=='body':
            if not self.body:
                self.body = Text_Extractor.extract_body(self.html)
                self.body = URLUtility.clean_text(self.body)
            return self.body
        elif text_type=='meta':
            if not self.meta:
                self.meta = Text_Extractor.extract_body(self.html)
                self.meta = URLUtility.clean_text(self.meta)
            return self.meta
        elif text_type=='title':
            if not self.title:
                self.title = Text_Extractor.extract_body(self.html)
                self.title = URLUtility.clean_text(self.title)
            return self.title

        else:
            print "Wrong text_type"
            return ''

    def load_from_json(self, json_obj):
        """
        Don't load the json object if it is not valid (e.g., too large or lacking of title)
        """
        """
        if json_obj['url'] == "http://www.armslist.com/classifieds/knoxville-tennessee":
            print json_obj
            print self.is_valid(json_obj)
            print json_obj['text']
        """
        if not json_obj:
            print "Warning: json object is empty"
            return
    
        if 'html' in json_obj:
            if self.is_valid(json_obj):
                self.html = json_obj['html']
                if 'text' in json_obj:
                    self.body = json_obj['text']
        else:
            print 'html is empty'

    def is_valid(self, json_obj):
        """
        Is the json_obj valid?

        Return False if:
        - html is too small
        - html is too large (potentially not valid html)
        - title is empty (not legitimate html page) 
        """
        if len(json_obj['html']) < 200:
            return False

        if len(json_obj['html']) >= self.max_html_size:
            print "Warning: skip large html, ", json_obj['url']
            return False
        
        """
        # TODO: Fix title extraction
        title = Text_Extractor.extract_title(json_obj['html']).lower()
        if not title:
            #print "Skipped url because of an empty title,", json_obj['url']
            return False
        """

        return True

    def get_json_obj(self):
        return {'url':self.url, 'text':self.get_text('body'), 'html':self.html}

    def get_word_set(self, text_type):
        """ 
        Extract text from html and tokenize it

        Returns:
        --------
        self.word_set: a set of tokens
        """ 
        if not self.word_set:
            stop = stopwords.words('english')
            words = word_tokenize(self.get_text(text_type))
            self.word_set = set([word for word in words if word not in stop])
        return self.word_set

    def get_vsm(self, vectorizer, text_type):
        """
        Extract text from html and Vectorize it using vectorizer

        Returns:
        --------
        self.vsm: a list of real numbers for representing the text
        """
        if not self.vsm:
            text = self.get_text(text_type)
            vsm_list = vectorizer.transform([text]).todense()
            #TODO: can't flatten vsm_list. The following code couldn't flatten vsm_list
            #self.vsm = vsm_list.flatten() or self.vsm = vsm_list.ravel()
            self.vsm = vsm_list.tolist()[0]
        return self.vsm

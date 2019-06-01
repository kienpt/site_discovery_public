import url_normalize
from urlutility import URLUtility
from page import Page

class Website(object):
    def __init__(self, url):
        #url = url_normalize.url_normalize(url)
        self.host = URLUtility.get_host(url)
        self.pages = []
        self.word_set = set()
        self.vsm = None
        self.jaccard = None # Don't use this if seeds are updated
        self.cosine = None # Don't use this if seeds are updated
        self.clf_vsm = None
        self.bstf_vsm = None
        self.bsbin_vsm = None
        self.cs_vsm = None

    def __key(self):
        return self.get_url()

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def get_url(self):
        if not self.pages:
            return ""
        else:
            return self.pages[0].get_url()

    def add_page(self, page):
        self.pages.append(page)

    def clear(self):
        self.vsm = None
        for page in self.pages:
            page.clear()

    def get_crawltime(self):
        """
        Return the crawl time of the first url
        """
        return self.pages[0].get_crawltime()

    def to_vector(self, vectorizer, text_type):
        """
        Transform website to a vector representation

        Returns:
        --------
        List of real numbers as a vector
        """
        if not self.pages:
            return []
        # Use a random page as website representation
        text = self.pages[0].get_text(text_type)
        vsm_list = vectorizer.transform([text]).todense()
        return vsm_list.tolist()[0]

    def get_word_set(self, text_type):
        """
        Union word from individual pages in a single set
        """
        if not self.word_set:
            self.word_set = set()
            for p in self.pages:
                self.word_set.update(p.get_word_set(text_type))
        return self.word_set

    def get_vsm(self, vectorizer, text_type):
        """
        Extract text from html and Vectorize it using vectorizer

        Returns:
        --------
        self.vsm: a list of real numbers for representing the text
        """
        if self.vsm is None:
            text = [p.get_text(text_type) for p in self.pages]
            text = ' '.join(text)
            vsm_list = vectorizer.transform([text]).todense()
            #TODO: can't flatten vsm_list. The following code couldn't flatten vsm_list
            #self.vsm = vsm_list.flatten() or self.vsm = vsm_list.ravel()
            self.vsm = vsm_list.tolist()[0]
        return self.vsm

    def get_clf_vsm(self, vectorizer, text_type):
        """
        Extract text from html and Vectorize it using vectorizer

        Returns:
        --------
        self.vsm: a list of real numbers for representing the text
        """
        if self.clf_vsm is None:
            text = [p.get_text(text_type) for p in self.pages]
            text = ' '.join(text)
            vsm_list = vectorizer.transform([text]).todense()
            #TODO: can't flatten vsm_list. The following code couldn't flatten vsm_list
            #self.vsm = vsm_list.flatten() or self.vsm = vsm_list.ravel()
            self.clf_vsm = vsm_list.tolist()[0]

        return self.clf_vsm

    def get_bstf_vsm(self, vectorizer, text_type):
        """
        Extract text from html and Vectorize it using vectorizer

        Returns:
        --------
        self.vsm: a list of real numbers for representing the text
        """
        if self.bstf_vsm is None:
            text = [p.get_text(text_type) for p in self.pages]
            text = ' '.join(text)
            vsm_list = vectorizer.transform([text]).todense()
            #TODO: can't flatten vsm_list. The following code couldn't flatten vsm_list
            #self.vsm = vsm_list.flatten() or self.vsm = vsm_list.ravel()
            self.bstf_vsm = vsm_list.tolist()[0]

        return self.bstf_vsm

    def get_bsbin_vsm(self, vectorizer, text_type):
        """
        Extract text from html and Vectorize it using vectorizer

        Returns:
        --------
        self.vsm: a list of real numbers for representing the text
        """
        if self.bsbin_vsm is None:
            text = [p.get_text(text_type) for p in self.pages]
            text = ' '.join(text)
            vsm_list = vectorizer.transform([text]).todense()
            #TODO: can't flatten vsm_list. The following code couldn't flatten vsm_list
            #self.vsm = vsm_list.flatten() or self.vsm = vsm_list.ravel()
            self.bsbin_vsm = vsm_list.tolist()[0]

        return self.bsbin_vsm

    """
    def get_cs_vsm(self, vectorizer, text_type):
        if self.cs_vsm is None:
            text = [p.get_text(text_type) for p in self.pages]
            text = ' '.join(text)
            vsm_list = vectorizer.transform([text]).todense()
            #TODO: can't flatten vsm_list. The following code couldn't flatten vsm_list
            #self.vsm = vsm_list.flatten() or self.vsm = vsm_list.ravel()
            self.cs_vsm = vsm_list.tolist()[0]
        else:
            print "hit vsm cosine"

        return self.cs_vsm
    """

    def get_host(self):
        return self.host

    def load_from_json(self, json_obj):
        """
        Populate data from a json object, which contains list of pages

        Returns 
        -------
        None
        """
        for json_page in json_obj:
            page = Page(json_page['url'])
            page.load_from_json(json_page)
            if not page.is_empty():
                self.pages.append(page)

    def get_json_obj(self):
        obj = []
        for page in self.pages:
            obj.append(page.get_json_obj())
        return obj

    def __iter__(self):
        return iter(self.pages)

    def is_empty(self):
        """
        Return True if the website does not have any page
        """
        return False if self.pages else True

from boilerpipe.extract import Extractor
from bs4 import BeautifulSoup
import traceback
import re

title_pattern = re.compile("<title>(.*?)</title>", re.IGNORECASE)

class Text_Extractor:
    def __init__(self):
        # Choice of extrators, Boilerpipe, xpath, beautiful_soup or customized extractor?
        pass

    @staticmethod
    def extract_title(html):
        """
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find('title')
        title_text = title.text if title else ""
        return title_text.strip()
        """
        # regex is an order of magnitude faster than beautifulsoup when extracting title
        try:
            res = title_pattern.search(html)
            if res:
                return res.group(1).strip()
            else:
                return ""
        except:
            traceback.print_exc()
            return ""

    @staticmethod
    def extract_metadata(html):
        """
        Extract title, description, keywords

        Returns:
        --------
        a lower case string that is the concatination of title, desc and keywords.
        """
        try:
            metadata = []
            soup = BeautifulSoup(html, 'lxml')
            title = soup.find('title')
            title_text = title.text if title else ""
            metadata.append(title_text.strip())
            
            metatags = soup.find_all('meta')
            for tag in metatags:
                if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description', 'keywords']:
                    try:
                        metadata.append(tag.attrs['content'].strip())
                    except:
                        print tag.attrs.keys()

            res = ' '.join(metadata) 
            if not res:
                print "Empty Metadata"
            return res
        except:
            print "Metadata extraction fails"
            return ""

    @staticmethod
    def extract_body(html, type="beautifulsoup"):
        if type=="beautifulsoup":
            return Text_Extractor.extract_body_with_beautifulsoup(html)
        elif type=="boilerpipe":
            return Text_Extractor.extract_body_with_boilerpipe(html)
        else:
            print "Wrong extraction type"
            return ""

    @staticmethod
    def extract_body_with_beautifulsoup(html):
        """
        Extract text using BeautifulSoup Library
        """ 
        """
        def tag_visible(element):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, Comment):
                return False
            return True
        """

        try:
            soup = BeautifulSoup(html, "lxml")
            #texts = soup.findAll(text=True)
            #visible_texts = filter(tag_visible, texts)
            #return " ".join(t.strip() for t in visible_texts)
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            text = " ".join(text.split())
            return text
        except:
            print "Text extraction with beautiful soup failed"
            return ""

    @staticmethod
    def extract_body_with_boilerpipe(html):
        """
        Extractor types:
                DefaultExtractor
                ArticleExtractor
                ArticleSentencesExtractor
                KeepEverythingExtractor
                KeepEverythingWithMinKWordsExtractor
                LargestContentExtractor
                NumWordsRulesExtractor
                CanolaExtractor
        Reference: https://github.com/misja/python-boilerpipe
        Note: set JAVA_HOME if import fails

        Returns
        --------
        str: extracted body text. Return empty string if extraction fails
        """
        try:
            extractor = Extractor(extractor='KeepEverythingExtractor', html=html)
            extracted_text = extractor.getText()
        except:
            print "Failed to extract text with boilerpipe"
            extracted_text = ""

        return extracted_text

def test_extract_title():
    html = "\r\n        <title>\r\n    \r\n    ARMSLIST - Knoxville Firearms Classifieds\r\n\r\n</title>\r\n  "
    title = Text_Extractor.extract_title(html)
    if not title:
        print  "title extraction failed"

def test():
    import requests
    url = "http://nyu.edu"
    res = requests.get(url)
    html = res.text
    print "Extracting text from ", url
    print "Using Boilerpipe"
    text = Text_Extractor.extract_body(html, "boilerpipe")
    print text
    #print text.replace("\n", "")
    print "Using beautifulsoup"
    text = Text_Extractor.extract_body(html, "beautifulsoup")
    print text

if __name__=="__main__":
    test()

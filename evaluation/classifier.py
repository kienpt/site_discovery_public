"""
A classifier to evaluate the discovery results

training_data
    |
     __ positive/data.json
    |
     __ negative/data.json
"""
import os
import sys
import json
import traceback
import argparse
import numpy as np
import cPickle as pickle
from  sklearn.svm import SVC
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append('utils')
sys.path.append("extraction")
sys.path.append("ranking")
from urlutility import URLUtility
from multiproc_fetcher import Fetcher
from text_extractor import Text_Extractor
from lemma_tokenizer import LemmaTokenizer

def load_data(data_path):
    """ 
    Two format of data_path:
        1. Contain single json line file: data.json
        2. Contain html files - ache format
    """ 
    docs = []
    data_file = data_path + '/data.json'
    if os.path.isfile(data_file):
        with open(data_file) as lines:
            for line in lines:
                js = json.loads(line)
                if 'text' in js:
                    text = js['text']
                else:
                    html = js['html']
                    text = Text_Extractor.extract_body(html).lower()                 
                text = URLUtility.clean_text(text)
                if text:
                    docs.append(text)
    else:
        files = os.listdir(data_path)
        idx = 0
        for f in files:
            idx += 1
            if idx%100==0:
                print "Processed ", idx
            try:
                filepath = data_path + '/' + f
                html = open(filepath).read()
                text = Text_Extractor.extract_body(html).lower()                 
                text = URLUtility.clean_text(text)
                if text and len(text)>200:
                    docs.append(text)
            except:
                traceback.print_exc()

    print "Loaded ", len(docs)
    return docs

def train(data_dir, model_file, vect_file, is_test=False):
    """
    data_dir must contain 2 directories: positive and negative
    Each directory must contain a json file (i.e., data.json) or list of html files (ache format)
    """
    print "Loading data..."
    pos_docs = load_data(data_dir + '/positive')
    neg_docs = load_data(data_dir + '/negative')
    docs = pos_docs + neg_docs

    print "Vectorizing..."
    #vectorizer = TfidfVectorizer(tokenizer=LemmaTokenizer(), stop_words='english', ngram_range=(1,2), max_df=0.95, min_df=0.05, norm='l2', sublinear_tf=True)
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_df=0.97, min_df=0.03, norm='l2', sublinear_tf=False)
    vectorizer.fit(docs) 
    pos = vectorizer.transform(pos_docs).todense()
    neg = vectorizer.transform(neg_docs).todense()
    print pos.shape, neg.shape
    x = np.concatenate((pos, neg))
    y = np.array([1]*pos.shape[0] + [-1]*neg.shape[0])
    x, y = shuffle(x, y, random_state=0)

    #clf = SVC(kernel="linear", gamma=0.01, C=0.005, probability=True) # much worse compared to default gamma and C
    clf = SVC(kernel="linear", C=1.3, probability=True)

    print "Fitting..."
    if is_test:
        scores = cross_val_score(clf, x, y, cv=5) 
        print "Cross validation score: ", scores
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    clf.fit(x, y)

    print "Saving..."
    with open(model_file, 'wb') as f:
        pickle.dump(clf, f)
    with open(vect_file, 'wb') as f:
        pickle.dump(vectorizer, f)

def evaluate(url_file, data_dir, model_file, vect_file, result_file):
    """ 
    Args:
        url_file: list of urls to evaluate
        data_dir: directory contains 
    """
    clf = pickle.load(open(model_file, "rb"))
    vectorizer = pickle.load(open(vect_file, "rb"))
    urls = URLUtility.load_urls(url_file, col=0, sep=',')
    print "Number of urls to evaluate: ", len(urls)

    fetcher = Fetcher(data_dir)
    pages = fetcher.fetch_pages(urls) 
    vects = [p.get_vsm(vectorizer, 'body') for p in pages]
    predictions = clf.predict(vects)
    out = open(result_file, 'w')
    for i in xrange(len(pages)):
        out.write(pages[i].get_url() + ',' + str(predictions[i]) + '\n')
    out.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-td", "--traindir", help="path to training data directory", type=str)
    parser.add_argument("-md", "--modeldir", help="path to model directory", type=str)
    parser.add_argument("-ed", "--evaldir", help="path to evaluation data directory", type=str)
    parser.add_argument("-res", "--resfile", help="path to evaluation data directory", type=str)
    parser.add_argument("-u", "--urlfile", help="file with urls of pages to evaluate", type=str)
    #parser.add_argument("-mp", "--maxpages", help="Maximal number of pages selected in a website, excluded the homepage", type=int)
    #parser.add_argument("-o", "--online", action='store_true') # default = False
    parser.add_argument("-t", "--test", action='store_true') # default = False
    parser.add_argument("-a", "--action", help="train, evaluate", type=str)
    args = parser.parse_args()

    if not os.path.exists(args.modeldir):
        os.makedirs(args.modeldir)
    model_file = args.modeldir + '/model.dat'
    vect_file = args.modeldir + '/vect.dat'

    if args.action == 'train':
        if not os.path.exists(args.traindir):
            os.makedirs(args.traindir)
        train(args.traindir, model_file, vect_file, args.test)
    elif args.action == 'evaluate':
        evaluate(args.urlfile, args.evaldir, model_file, vect_file, args.resfile)

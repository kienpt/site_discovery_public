from math import sqrt
from numpy import *
import numpy as np
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from lemma_tokenizer import LemmaTokenizer

class Bayesian_Sets(object):

    def __init__(self, seeds, representation, value_type, decomposition=None):
        """
        Parameters
        ----------
        value_type : "tfidf" or "binary "
        decomposition: "pca", "nmf", "lsa"
        """
        self.text_type = representation
        # min_df = 2: filter any token that appears in less than 2 documents
        # min_df = 0.125: filter any token that apearrs in less than 0.125*number_of_docs documents
        mdf = max(2/float(len(seeds)), 0.1)  
        # Create vectorizer
        self.value_type = value_type
        if value_type=="binary":
            #self.vectorizer = CountVectorizer(binary=True, stop_words='english', ngram_range=(1,2))
            #self.vectorizer = CountVectorizer(binary=True, stop_words='english', ngram_range=(1,2), max_df=0.75, min_df=0, max_features=1000)
            self.vectorizer = CountVectorizer(binary=True, stop_words='english', ngram_range=(1,2), max_df=1.0, min_df=mdf)
        elif value_type=="tfidf":
            #self.vectorizer = TfidfVectorizer(tokenizer=LemmaTokenizer(), stop_words='english', ngram_range=(1,2), max_df=1.0, min_df=mdf, use_idf=False, norm='l1', sublinear_tf=True)
            self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_df=1.0, min_df=mdf, use_idf=False, norm='l1', sublinear_tf=False)
        else:
            print "Wrong value type of Bayesian Sets."
            sys.exit()
        self.seeds = seeds
        self.vect_seeds = self._vectorize_seeds()
        for i, v in enumerate(self.vect_seeds):
            print self._count(v)

        print "Initialized Bayesian sets object. text type = ", self.text_type

        #decomposition = 'nmf'  # uncomment to use decomposition. Only NMF works because bayesian sets require non-negative inputs
        if decomposition=='nmf':
            self.model = NMF(n_components=200, init='nndsvd', random_state=0)
            print "Created nmf model"
        elif decomposition == 'pca':
            self.model = PCA(n_components=100)
            print "Created pca model"
        elif decomposition == 'lsa':
            self.model = TruncatedSVD(n_components=100) 
            print "Created lsa model"

        self.decomposition = decomposition

    def _count(self, vect):
        c = 0
        for i in vect:
            if i:
                c += 1
        return c

    def _vectorize_seeds(self):
        print "Vectorizing seed websites..."
        docs = [] # list of strings, used for constructing vectorizer
        for w in self.seeds:
              docs.extend([p.get_text(self.text_type) for p in w])
        #self.vect_seeds = self.vectorizer.fit_transform(docs).todense() # Why converting to dense vector?
        self.vectorizer.fit(docs) 
        if self.value_type=="tfidf":
            return np.array([w.get_bstf_vsm(self.vectorizer, self.text_type) for w in self.seeds])
        elif self.value_type=="binary":
            return np.array([w.get_bsbin_vsm(self.vectorizer, self.text_type) for w in self.seeds])
        else:
            print "Wrong value type"
            return None

    def update_seeds(self, new_seeds):
        self.seeds.extend(new_seeds)
        for w in self.seeds:
            w.clear()
        self.vect_seeds = self._vectorize_seeds()

    def score(self, websites): 
        print "Scoring..."
        if self.value_type=="tfidf":
            X = np.array([w.get_bstf_vsm(self.vectorizer, self.text_type) for w in websites])
        elif self.value_type=="binary":
            X = np.array([w.get_bsbin_vsm(self.vectorizer, self.text_type) for w in websites])
        else:
            print "Wrong value type"
        print 'Shape ', X.shape
        if self.decomposition:
            self.vect_seeds, X = self._reduce_dim(self.vect_seeds, X)

        scores = self.score_helper(self.vect_seeds, X)
        results = []
        for i, w in enumerate(websites):
            results.append((w, scores[i]))  
        return results

    def _reduce_dim(self, T, X): 
        """
        Use decomposition method to reduce dimension of the two vectors T and X.
        Concatenate T and X and apply decomposition to the combined vector.
        """
        TX = np.concatenate((T, X), axis=0)
        print "Transforming"
        transformed_X = self.model.fit_transform(TX)
        print "Done transform"
        split = T.shape[0]
        new_T, _, new_X = np.vsplit(transformed_X, (split, split))
        return new_T, new_X

    def _reduce_dim_separated(self, T, X): 
        print "Transforming"
        new_T = self.model.fit_transform(T)
        new_X = self.model.fit_transform(X)
        print "Done transform"
        return new_T, new_X

    def score_helper(self, D, X) :
        ''' D-> Query Set
            X-> Data Set'''
        #Compute Bayesian Sets Parameters
        c = 2
        N = D.shape[0]
        T = concatenate((D,X), axis=0)
        m = divide(sum(T, axis=0),float(T.shape[0]))

        a = multiply(m, c)
        b = multiply(subtract(1,m),c)

        at = add(a,sum(D, axis=0))
        bt = subtract(add(b,N),sum(D, axis=0))
        
        C = sum(subtract(add(subtract(log(add(a,b)),log(add(add(a,b),N))), log(bt)), log (b)))
        q = transpose(add(subtract(subtract(log(at),log(a)),log(bt)), log(b)))
        score_X = transpose(add(C, dot(X,q)))
        return asarray(score_X)

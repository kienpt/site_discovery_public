from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
import numpy as np
from numpy.linalg import norm
#from sklearn.decomposition import NMF
#from sklearn.decomposition import PCA
#from sklearn.decomposition import TruncatedSVD

class Cosine_Similarity(object):
    """
    Note: all text is lower case 
    """
    def __init__(self, seeds, representation, decomposition=None):
        """
        Note: decomposition and update_seeds do not work together
        """
        self.seeds = seeds
        #self.text_type = config['RANKING_EVALUATION']['TextType']
        self.text_type = representation
        # Create vectorizer
        #self.vectorizer = TfidfVectorizer(stop_words='english')
        mdf = max(2/float(len(seeds)), 0.1)  
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_df=1.0, min_df=mdf, use_idf=False)

        self.seeds = seeds
        self.T = self._vectorize()# T is only used for decomposition

        print "Initialized Cosine Similarity object. text type = ", self.text_type
        
        #decomposition = 'nmf'
        """
        if decomposition=='nmf':
            self.model = NMF(n_components=400, init='nndsvd', random_state=0)
            print "Created nmf model"
        elif decomposition == 'pca':
            self.model = PCA(n_components=200)
            print "Created pca model"
        elif decomposition == 'lsa':
            self.model = TruncatedSVD(n_components=200) 
            print "Created lsa model"

        self.decomposition = decomposition
        """
        self.decomposition = None # Server does not have some decomposition library so disable this for now to avoid import exception 

    def _vectorize(self):
        print "Vectorizing seed websites..."
        docs = [] # list of strings
        for w in self.seeds:
            docs.extend([p.get_text(self.text_type) for p in w])
        return self.vectorizer.fit_transform(docs).toarray() 

    def update_seeds(self, new_seeds):
        self.seeds.extend(new_seeds)        
        for w in self.seeds:
            w.clear()
        self._vectorize()

    def score(self, websites):
        """
        Args:
            - websites: List[Website]
        Returns: 
            List[List[float, Website]]
        """
        print "Scoring..."
        results = []
        if self.decomposition:
            X = np.array([w.get_vsm(self.vectorizer, self.text_type) for w in websites])
            self.T, X = self._reduce_dim(self.T, X)
            scores = cosine_similarity(X, self.T) 
            scores =  np.mean(scores, axis=1).tolist()
            results = [(websites[i], scores[i]) for i in xrange(len(scores))]
        else:
            for i, website in enumerate(websites):
                if website.cosine is None:
                    scores = [self._union(website, s) for s in self.seeds]
                    website.cosine = sum(scores)/len(scores) if scores else 0
                results.append((website, website.cosine))

        return results

    def _reduce_dim(self, T, X): 
        """
        Use decomposition method to reduce dimension of the two vectors T and X.
        Concatenate T and X before running NMF.
        """
        TX = np.concatenate((T, X), axis=0)
        print "Transforming"
        transformed_X = self.model.fit_transform(TX)
        print "Done transform"
        split = T.shape[0]
        new_T, _, new_X = np.vsplit(transformed_X, (split, split))
        return new_T, new_X

    def _smd(self, w1, w2):
        '''
        Use Sum of Minimum Distance method (SMD) to compute the similarity between two sites
        '''
        docs1 = np.array([p.get_vsm(self.vectorizer, self.text_type) for p in w1])
        docs2 = np.array([p.get_vsm(self.vectorizer, self.text_type) for p in w2])
        scores = cosine_similarity(docs1, docs2)

        max_scores1 = [0]*len(docs1)
        max_scores2 = [0]*len(docs2)
        for i in xrange(len(scores)):
            for j in xrange(len(scores[0])):
                max_scores1[i] = max(max_scores1[i], scores[i][j])
                max_scores2[j] = max(max_scores2[j], scores[i][j])

        sum_scores = sum(max_scores1) + sum(max_scores2)
        n = len(max_scores1) + len(max_scores2)
        return sum_scores/float(n) if n else 0

    def _union(self, w1, w2):
        v1 = w1.get_vsm(self.vectorizer, self.text_type)
        v2 = w2.get_vsm(self.vectorizer, self.text_type)
        score = cosine_similarity([v1], [v2])
        return score[0][0]
        #cos_sim = np.dot(v1, v2)/(norm(v1)*norm(v2))
        #return cos_sim

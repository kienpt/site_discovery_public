class Jaccard_Similarity(object):
    def __init__(self, seeds, representation):
        self.seeds = seeds # list of seed websites
        #self.text_type = config['RANKING_EVALUATION']['TextType']
        self.text_type = representation
        print "Initialized Jaccard Similarity object. text type = ", self.text_type

    def update_seeds(self, new_seeds):
        self.seeds.extend(new_seeds)

    def score(self, websites):
        """
        Args:
            - websites: List[Website]
        Returns: 
            List[List[float, Website]]

        Note:
            This function uses pre-computed jaccard similarity, therefore if seeds are updated, this need to be changed.
        """
        print "Scoring..."
        results = []
        for i, website in enumerate(websites):
            #scores = [self._smd(website, s) for s in self.seeds]
            if website.jaccard is None:
                scores = [self._union(website, s) for s in self.seeds]
                website.jaccard = sum(scores)/len(scores) if scores else 0
            #if i%800==0:
            #    print "Computing similarity...  Completed ", i, " sites" 
            results.append((website, website.jaccard))
        return results

    def _smd(self, w1, w2):
        """
        Use Sum of Minimum Distance method (SMD) to compute the similarity between two sites
        """
        max_scores1 = [0]*len(w1.pages)
        max_scores2 = [0]*len(w2.pages)
        for i, page1 in enumerate(w1):
            for j, page2 in enumerate(w2):
                score = self._jaccard(page1.get_word_set(self.text_type), page2.get_word_set(self.text_type))
                max_scores1[i] = max(max_scores1[i], score)
                max_scores2[j] = max(max_scores2[j], score)
        sum_scores = sum(max_scores1) + sum(max_scores2)
        n = len(max_scores1) + len(max_scores2)
        sim = sum_scores/float(n) if n else 0
        return sim

    def _union(self, w1, w2):
        """
        Union all pages to create representation of a website
        """
        score = self._jaccard(w1.get_word_set(self.text_type), w2.get_word_set(self.text_type))
        return score

    def _jaccard(self, s1, s2):
        """
        Compute jaccard similarity between two sets
        """
        if (not s1) and (not s2):
            #print "Warning: two sets are empty"
            return 0
        return len(s1.intersection(s2))/float(len(s1.union(s2)))

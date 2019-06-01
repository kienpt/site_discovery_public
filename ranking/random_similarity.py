'''
This class is used as a random ranking baseline
'''
import random
class Random_Similarity(object):
    def __init__(self, seeds):
        self.seeds = seeds # list of seed websites

    def score(self, websites):
        '''
        Args:
            - websites: List[Website]
        Returns: 
            List[List[float, Website]]
        '''
        results = []
        n = len(websites)
        scores = [i for i in xrange(n)]
        random.shuffle(scores)
        for i, score in enumerate(scores):
            results.append((websites[i], score))

        return results

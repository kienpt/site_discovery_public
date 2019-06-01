import math
"""
Batched ucb
"""

class UCB1(object):
    def __init__(self, arms):
        self.counts = {arm:0 for arm in arms}
        self.values ={arm:0.0 for arm in arms} # averaged reward
        self.n_arms = len(arms)
    
    def select_arm(self):
        print "UCB Counts ", self.counts
        print "UCB Values ", self.values
        for arm in self.counts:
            if self.counts[arm] == 0:
                return arm

        ucb_values = {arm:0.0 for arm in self.counts}
        total_counts = sum(self.counts.values())
        for arm in self.counts:
            bonus = math.sqrt((2 * math.log(total_counts)) / float(self.counts[arm]))
            ucb_values[arm] = self.values[arm] + bonus
        print "UCB UCBScores ", ucb_values
        return max(ucb_values, key=ucb_values.get)
    
    def update(self, chosen_arm, reward, k):
        self.counts[chosen_arm] += k
        #self.counts[chosen_arm] += 1
        n = self.counts[chosen_arm]

        value = self.values[chosen_arm]
        new_value = ((n - k) * value + k * reward)/float(n)
        self.values[chosen_arm] = new_value

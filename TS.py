import numpy as np
import scipy as sp
import pickle
from scipy.stats import beta
from MAB import MAB

class TS(MAB):
    def __init__(self, itemid, posProb):
        super(TS,self).__init__(itemid, posProb)
        self.S = [0 for _ in range(self.K)]  #clicks
        self.N = [0 for _ in range(self.K)]  #imps

    #return sorted list of item numbers, with length require_num
    def select_items(self, required_num):
        self.turn += 1
        beta_val = [0.0] * self.K  #initialize beta_draw value for arms
        for k in range(self.K):
            beta_val[k] = np.random.beta(self.S[k] + 1, self.N[k] - self.S[k] + 1)  #beta_draw with (click, unclick) for each arms
            items = sorted([(beta_val[k], k) for k in range(self.K)], reverse=True)
            result = [items[i][1] for i in range(required_num)]
            return result

    def update(self, selected_items, feedback):
        assert len(selected_items) == len(feedback)
        for l in range(len(selected_items)):
            k = selected_items[l]
            self.N[k] += 1  #imps += 1
            if feedback[l]:
                self.S[k] += 1  #if feedback, then clicks += 1

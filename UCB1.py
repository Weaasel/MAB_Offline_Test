import numpy as np
import scipy as sp
import pickle
from scipy.stats import beta
from MAB import MAB

class UCB1(MAB):
    def __init__(self, itemid, select_num):
        super(UCB1,self).__init__(itemid, select_num)
        self.S = [0 for _ in range(self.K)]  #clicks
        self.N = [0 for _ in range(self.K)]  #imps
        self.initList = [i for i in range(self.K)]

    #return sorted list of item numbers, with length require_num
    def select_items(self, required_num):
        self.turn += 1
        items, result = [], []
        while len(result) < required_num and len(self.initList)>0:
            result.append(self.initList[-1])
            self.initList.pop()
        for i in range(self.K):
            if self.N[i] == 0:continue
            items.append((self.S[i]/self.N[i] + (2*np.log(self.turn)/self.N[i])**0.5, i))
        items = sorted(items, reverse=True)
        for i in range(len(items)):
            if len(result) == required_num: break
            if items[i][1] in result: continue
            result.append(items[i][1])
        return result

    def update(self, selected_items, feedback, clicked_idx):
        assert len(selected_items) == len(feedback)
        for l in range(clicked_idx+1):
            k = selected_items[l]
            self.N[k] += 1  #imps += 1
            if feedback[l]:
                self.S[k] += 1  #if feedback, then clicks += 1

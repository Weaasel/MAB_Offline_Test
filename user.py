import numpy as np

class User:
    def __init__(self, select_num, itemProb):
        self.L = select_num
        self.K = len(itemProb)
        self.itemProb = itemProb

    #for each items, user makes clicked or unclicked with itemProb
    def react(self, items, itemProb_idx):
        assert len(items) == self.L
        clicked = [False for _ in range(self.L)]
        for i in range(self.L):
            if 0 == np.random.binomial(1, self.itemProb[itemProb_idx][items[i]]): continue
            clicked[i] = True
            return clicked, i
        return clicked, len(clicked)-1

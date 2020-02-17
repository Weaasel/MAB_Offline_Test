import numpy as np
from MAB import MAB
class Monitord_TS(MAB):
    def __init__(self, itemid, select_num, rng = 4, b = 0.005):
        super(Monitord_TS,self).__init__(itemid, select_num)
        self.S = [0 for _ in range(self.K)]  #clicks
        self.N = [0 for _ in range(self.K)]  #imps
        self.rng = rng
        self.threshod = b
        self.obs = [[] for _ in range(self.K)]
        self.monitord = [0 for i in range(self.K)]

    #return sorted list of item numbers, with length require_num
    def select_items(self, required_num):
        self.turn += 1
        beta_val = [0.0] * self.K  #initialize beta_draw value for arms
        for k in range(self.K):
            beta_val[k] = np.random.beta(self.S[k] + 1, self.N[k] - self.S[k] + 1)  #beta_draw with (click, unclick) for each arms
        items = sorted([(beta_val[k], k) for k in range(self.K)], reverse=True)
        result = [items[i][1] for i in range(required_num)]
        return result

    def update(self, selected_items, feedback, clicked_idx):
        assert len(selected_items) == len(feedback)
        for l in range(clicked_idx+1):
            k = selected_items[l]
            self.N[k] += 1  #vimps += 1
            if self.N[k] - self.monitord[k] > 10:  #monitoring with CTR starts when vimp >= 10
                self.obs[k].append(self.S[k] / (self.N[k] + self.N[k]))
                self.monitord[k] += self.N[k]
                if self.detect_change(self.obs[k]):
                    self.obs[k] = []
                    self.monitord[k] = 0
                    self.N[k] /= float(self.S[k])
                    self.S[k] /= float(self.S[k])
            if feedback[l]:
                self.S[k] += 1  #if feedback, then clicks += 1

    def detect_change(self, obs):
        flag = False
        if len(obs) < self.rng:
            return flag
        elif len(self.obs) > self.rng:
            obs = obs[1:]
        if self._detect_change(obs):
            flag = True
        return flag

    def _detect_change(self, obs):
        previous = obs[:len(obs) / 2]
        after = obs[len(obs) / 2:]
        if abs(sum(previous) - sum(after)) > self.threshod:
            print 'change detected'
            return True
        else:
            return False

import numpy as np
import scipy as sp
import random
import pickle

class MAB(object):
    def __init__(self, itemid, posProb):
        self.K = len(itemid)  #num of whole arms
        self.L = len(posProb)  #num of drawing arms in each turn
        self.turn = 0  #num of draws(turns)
        self.itemid = itemid  #list of itemids
        self.posProb = posProb  #list of position prob of items

    #return sorted list of item numvers with length require_num. Default Random
    def select_items(self, required_num):
        random.shuffle(self.itemid)
        return self.itemid[:required_num]

    def update(self, selected_items, feedback):
        pass

    def save(self, fname):
        with open(fname, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def load(self, fname):
        with open(fname, 'rb') as f:
            sim = pickle.load(f)
            self.__dict__.clear()
            self.__dict__.update(sim)

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from user import User
from MAB import MAB
from TS import TS
from UCB1 import UCB1

class Simulator:
    def __init__(self, itemid, posProb, itemProb):
        self.L = len(posProb)
        self.K = len(itemProb[0])
        self.itemid = itemid
        self.posProb = posProb
        self.itemProb = itemProb

    def save(self, fname):
        with open(fname, 'w') as f:
            pickle.dump(self, f)

    def load(self, fname):
        load_sim = pickle.load(fname)

        self.itemid = load_sim.itemid
        self.posProb = load_sim.posProb
        self.itemProb = load_sim.itemProb

    def run(self, arg):
        log_fname = arg.get('log_fname', None)
        save_graph = arg.get('save_graph', False)
        step_cnt = arg.get('step_cnt', 1000)
        user = User(self.posProb, self.itemProb)

        models = [
            TS(self.itemid, self.posProb),
            UCB1(self.itemid, self.posProb),
            MAB(self.itemid, self.posProb)  #current 3 models
        ]
        labels = ['TS', 'UCB1', 'Random']
        regret = [0.0] * len(models)
        plots = [[] for _ in range(len(models))]
        step = 0
        pointNum = 10000  #graph point_num
        base_step = []
        itemProb_shift = step_cnt/len(self.itemProb)  #itemProb shift timing
        print(itemProb_shift)
        while step < step_cnt:
            step += 1
            itemProb_idx = (step-1)/itemProb_shift
            if step % 10000 == 0:
                print(step, step_cnt)

            for i in range(len(models)):
                selected_items = models[i].select_items(self.L)  #select arms
                feedback = user.react(selected_items, itemProb_idx)  #get feedback with binomial draw
                models[i].update(selected_items, feedback)  #update click/unclick
                regret[i] += sum([self.posProb[l] * self.itemProb[itemProb_idx][l] for l in range(self.L)]) - feedback.count(True)  #calculate regret

            if step % max(1, (step / pointNum)) == 0:
               base_step.append(step)
               for i in range(len(models)):
                   plots[i].append(regret[i])

        #save regret graph
        if save_graph:
            plt.figure()
            for i in range(len(models)):
                plt.plot(base_step, plots[i], label=labels[i])
            plt.legend()
            plt.xlabel('step')
            plt.ylabel('regret')
            plt.savefig(log_fname+'graph.png')

        return base_step, np.array(plots)










import os
import time
import datetime
import pickle
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

from simulator import Simulator

def main():
    if not os.path.exists('log'):
        os.makedirs('log')
    
    start_time = time.time()
    select_num = 3
    itemProb = [
        [0.45, 0.44, 0.40, 0.25, 0.05],
#        [0.10, 0.20, 0.30, 0.40, 0.50],
#        [0.20, 0.70, 0.65, 0.60, 0.55],
#        [0.20, 0.60, 0.60, 0.60, 0.60],
#        [0.05, 0.10, 0.15, 0.20, 0.25],
#        [0.90, 0.30, 0.20, 0.10, 0.00],
#        [0.25, 0.80, 0.75, 0.70, 0.65],
#        [0.30, 0.40, 0.40, 0.30, 0.30],
#        [0.40, 0.40, 0.40, 0.40, 0.40],
#        [0.50, 0.50, 0.50, 0.50, 0.50]
    ]  #row: turn, col: arms

    K = len(itemProb[0])
    L = select_num
    itemid = [i for i in range(K)]

    expCount = 1
    stepCount = 5000
    sim = Simulator(itemid, select_num, itemProb)
    log_fname='log/'+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.')
    
    arg = {'step_cnt': stepCount, 'log_fname': log_fname}
    base, plots = sim.run(arg)
    for i in range(expCount-1):
        print(str(i+2)+'th exp')
        base, nowp = sim.run(arg)
        plots += nowp

    labels = ['TS', 'UCB1', 'Random']
    plt.figure()
    for i in range(len(labels)):
        plt.plot(base, list(plots[i]), label=labels[i])
    plt.legend()
    plt.xlabel('step')
    plt.ylabel('regret')
    plt.savefig(log_fname+'graph.png')

    plt.figure()
    for i in range(len(labels)-1):
        plt.plot(base, list(plots[i]), label=labels[i])
    plt.legend()
    plt.xlabel('step')
    plt.ylabel('regret')
    plt.savefig(log_fname+'graph_without_random.png')

    with open(log_fname+'txt', 'w') as f:
        f.write(str(('labels', labels, '# of arms', K, '# of pos', L, 'select_num', select_num, 'itemProb', itemProb, 'expCnt', expCount, 'stepCnt', stepCount)))

    with open(log_fname+'.plot.pickle', 'wb') as f:
        pickle.dump(plots,f)

    print('%s seconds' %(time.time() - start_time))

if __name__ == '__main__':
    main()

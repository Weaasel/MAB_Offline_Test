import os
import time
import datetime
import pickle
import cPickle
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing

from simulator import Simulator

def load_data(bandit):
    timestamp = [i for i in bandit]
    bandit_id = [i for i in bandit[timestamp[0]]][0]
    bandit_arms = {}

    for time in sorted(timestamp):
        arms = bandit[time][bandit_id]
        for arm in arms:
            if arm not in bandit_arms:
                bandit_arms[arm] = {}
            bandit_arms[arm][time] = arms[arm]
    result = []
    arm_ids = bandit[bandit.keys()[0]][bandit_id].keys()
    for arm_key in arm_ids:
        temp_bandit = bandit_arms[arm_key]
        time = temp_bandit.keys()
        
        ctr = [bandit_arms[arm_key][i]['click'] / (bandit_arms[arm_key][i]['click'] + bandit_arms[arm_key][i]['unclick']) if (bandit_arms[arm_key][i]['click'] + bandit_arms[arm_key][i]['unclick']) > 0 else 0 for i in time]
        time, ctr = zip(*sorted(zip(time, ctr)))
        result.append(list(ctr))
    mn = max([len(result[i]) for i in range(len(result))])
    result2 = []
    for i in result:
        if len(i) == mn:
            result2.append(i)
        else: pass
    return result2


def load_pickle(path):
    f = open(path)
    return cPickle.load(f)

def main():
    # load dataset
    bandit_path = './Data/mab_stack5.cPickle'
    bandit = load_pickle(bandit_path)
    
    data = load_data(bandit)
    data = np.array(data).T

    if not os.path.exists('log'):
        os.makedirs('log')
    
    start_time = time.time()
    select_num = 30
    itemProb = data
#    itemProb = [
#        [0.45, 0.44, 0.40, 0.25, 0.05],
#        [0.10, 0.20, 0.30, 0.40, 0.50],
#        [0.20, 0.70, 0.65, 0.60, 0.55],
#        [0.20, 0.60, 0.60, 0.60, 0.60],
#        [0.05, 0.10, 0.15, 0.20, 0.25],
#        [0.90, 0.30, 0.20, 0.10, 0.00],
#        [0.25, 0.80, 0.75, 0.70, 0.65],
#        [0.30, 0.40, 0.40, 0.30, 0.30],
#        [0.40, 0.40, 0.40, 0.40, 0.40],
#        [0.50, 0.50, 0.50, 0.50, 0.50]
#    ]  #row: turn, col: arms


    K = len(itemProb[0])
    L = select_num
    itemid = [i for i in range(K)]

    expCount = 50
    stepCount = 10000
    sim = Simulator(itemid, L, itemProb)
    log_fname='log/'+datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.')
    
    arg = {'step_cnt': stepCount, 'log_fname': log_fname}
    base, plots = sim.run(arg)
    for i in range(expCount-1):
        print(str(i+2)+'th exp')
        base, nowp = sim.run(arg)
        plots += nowp
    plots /= float(expCount)
    labels = ['TS', 'dgp', 'Monitord_TS', 'Random']
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

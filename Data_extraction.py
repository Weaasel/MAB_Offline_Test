import cPickle
import datetime
from matplotlib import pyplot as plt
import json

def _load(file_path):
    f = open(file_path)
    return cPickle.load(f)


if __name__ == '__main__':
    # for extraction from raw data
    data = _load('./Data/mab_stack5.cPickle')# raw data
    print "total timestamp length: %d" % len(data)
    timestamp = [i for i in data]
    bandit = [i for i in data[timestamp[0]]]
    bandit1 = bandit[0]
    bandit1_arms = {}
    for time in sorted(timestamp):
        arms1 = data[time][bandit1]
        for arm in arms1:
            if arm not in bandit1_arms:
                bandit1_arms[arm] = {}
            bandit1_arms[arm][time] = arms1[arm]

    for arm_key in bandit1_arms:
        print "arm_key=%s, num_timestamp=%d" % (arm_key, len(bandit1_arms[arm_key]))

    for arm_key in bandit1_arms:
        if len(bandit1_arms[arm_key]) > 70:
            timestamps = bandit1_arms[arm_key]
            ctr = []
            times = []
            for time in timestamps:
                times.append(time)
                #print "click: %d, unclick: %d"%(bandit1_arms[arm_key][time]['click'], bandit1_arms[arm_key][time]['unclick'])
                if bandit1_arms[arm_key][time]['click'] + bandit1_arms[arm_key][time]['unclick'] == 0:
                    continue
                ctr.append(bandit1_arms[arm_key][time]['click']/(bandit1_arms[arm_key][time]['click'] + bandit1_arms[arm_key][time]['unclick']))
            if len(ctr) == len(timestamps) and sum(ctr) > 0:

                print "timestamps len: %d, timestamps: %s" % (len(times), times)
                print "ctr len: %d, ctr: %s" % (len(ctr), ctr)
                times, ctr = zip(*sorted(zip(times, ctr)))
                times = [datetime.datetime.fromtimestamp(i) for i in times]
                plt.plot(times, ctr)
                plt.title(arm_key)
                plt.savefig(arm_key + '.png')
                plt.close()

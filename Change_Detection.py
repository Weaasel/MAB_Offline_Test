import numpy as np
import matplotlib.pyplot as plt
import cPickle
import datetime


class PH_t_modified:
    def __init__(self, epsilon, lamda):
        self.PH_obs_list = []
        self.PH_m_t = []
        # hyper-parameter: epsilon, lambda
        self.PH_epsilon = epsilon
        self.PH_lamda = lamda

    def detect_change(self, new_obs):
        flag = False
        self.PH_obs_list.append(new_obs)
        if len(self.PH_obs_list) < 4:
            return flag
        else:
            if self._detect_change(self.PH_obs_list):
                flag = True
        return flag

    def _detect_change(self, obs):
        x_bar = sum(obs) / float(len(obs))
        self.PM_m_t = [i - x_bar + self.PH_epsilon for i in obs]

        Max_t, Min_t = max(obs), min(obs)
        Max_PH_t = Max_t - obs[-1]
        Min_PH_t = obs[-1] - Min_t

        print "Max: %f, Min: %f, Current: %f" % (Max_t, Min_t, obs[-1])

        if Max_PH_t > self.PH_lamda:
            self.PH_obs_list = []
            self.PH_m_t = []
            print "Change detected by PH_max"
            return True
        elif Min_PH_t > self.PH_lamda:
            self.PH_obs_list = []
            self.PH_m_t = []
            print "Change detected by PH_min"
            return True
        else:
            return False


class Monitoring_CD:
    def __init__(self, rng, b):
        self.obs = []
        #hyper parameter
        self.rng = rng
        self.threshod = b

    def detect_change(self, new_obs):
        flag = False
        self.obs.append(new_obs)
        if len(self.obs) < self.rng:
            return flag
        elif len(self.obs) > self.rng:
            self.obs = self.obs[1:]

        if self._detect_change(self.obs):
            flag = True
        return flag

    def _detect_change(self, obs):
        previous = obs[:len(obs)/2]
        after = obs[len(obs)/2:]
        print previous, after
        print "prev= %f, aft= %f, statistic= %f" % (sum(previous), sum(after), abs(sum(previous) - sum(after)))
        if abs(sum(previous) - sum(after)) > self.threshod:
            self.obs = []
            print 'detected at statistic: %d'%abs(sum(previous) - sum(after))
            print 'change detected'
            return True
        else:
            return False

if __name__ == '__main__':
    # CD: parameter setting
    arg = {'PH_t': {'epsilon': 0.1,
                    'lamda': 0.01,
                    'minimum_obs': 6},
           'Monitoring': {'range': 4,
                          'threshold': 0.005}}

    CD = Monitoring_CD(arg['Monitoring']['range'], arg['Monitoring']['threshold'])
    CD = PH_t_modified(arg['PH_t']['epsilon'], arg['PH_t']['lamda'])

    for arm in data:
        CD = PH_t_modified(arg['PH_t']['epsilon'], arg['PH_t']['lamda'])
        timestamp, ctr = data[arm]['timestamp'], data[arm]['ctr']
        timestamp = [datetime.datetime.fromtimestamp(i) for i in timestamp]
        change_point = []
        plt.plot(timestamp, ctr)
        for idx, time in enumerate(timestamp):

            detected = CD.detect_change(ctr[idx])
            change_point.append(detected)
            if detected:
                plt.axvline(x=time, color = 'r', linestyle = '--')
        plt.show()


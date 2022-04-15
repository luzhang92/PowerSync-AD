# -*- encoding: utf-8 -*-
'''
@File    :  Task.py
@Time    :  2021/10/08 12:21:38
Author   :  Lu Zhang
@Version :  1.0
@Email   :  luzhang@sjtu.edu.cn
@Desc    :  The task class
'''
import json

## add random prediction error
import random

class Task():
    def __init__(self, name,create_time) -> None:
        self.name = name
        self.base_init = 0
        self.base_exec = 0
        self.init_ratio = []
        self.exec_ratio = []
        self.init = []
        self.exec = []
        self.create = create_time
        self.start = create_time
        self.end = 0
        self.duration = 0
        self.freq = []
        self.need_freq = []
        self.adjust_num = 0
        self.not_best_freq = 0
        self.best_freq = 8
        self.best_init_freq = 8
        self.best_exec_freq = 8
        self.init_phase = True
        self.coreid = -1
        self.last_freq = 0
        self.finished_run = 0
        self.finished_freqs = []
        self.true_best_init_freq = 8
        self.true_best_exec_freq = 8
        self.tru_best_freq = 8
        self.real_base_exec = 0

        self.total_duration = []
        self.total_duration_ratio = []

    def parse_function(self, path,scheme='other'):
        filename = path + self.name
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                sepred = line.split()
                init, expected_exec = int(sepred[0]), int(sepred[1])
                error_exec = int(expected_exec * 0.05)
                random_exec = random.randint(0,error_exec)
                exec = expected_exec + random_exec
                if self.base_init == 0:
                    self.base_init, self.base_exec, self.real_base_exec = init, expected_exec, exec
                    
                self.init.append(init)
                self.exec.append(exec)

                self.total_duration.append(init + exec)

                ratio_i = float(self.base_init) / init
                ratio_e = float(self.real_base_exec) / exec
                ratio_total = float((self.base_init + self.base_exec)/(init + expected_exec))
                self.init_ratio.append(ratio_i)
                self.exec_ratio.append(ratio_e)
                self.total_duration_ratio.append(ratio_total)

        with open(path+'frequency_requirement.json','r') as f:
            freq_requirement = json.load(f)
            self.best_init_freq = freq_requirement[self.name][0]
            self.best_exec_freq = freq_requirement[self.name][1]
            self.best_freq = self.best_init_freq
        if scheme == 'per-app':
            with open(path+'frequency_requirement_total.json','r') as f:
                freq_requirement = json.load(f)
                self.true_best_init_freq = freq_requirement[self.name][0]
                self.true_best_exec_freq = freq_requirement[self.name][1]
                self.true_best_freq = self.true_best_init_freq
        else:
            with open(path+'frequency_requirement.json','r') as f:
                freq_requirement = json.load(f)
                self.true_best_init_freq = freq_requirement[self.name][0]
                self.true_best_exec_freq = freq_requirement[self.name][1]
                self.true_best_freq = self.true_best_init_freq

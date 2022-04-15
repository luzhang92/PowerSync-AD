# -*- encoding: utf-8 -*-
'''
@File    :  Core.py
@Time    :  2021/10/08 18:48:02
Author   :  Lu Zhang
@Version :  1.0
@Email   :  luzhang@sjtu.edu.cn
@Desc    :  None
'''
import numpy as np
import Constant

class Core():
    def __init__(self, id) -> None:
        self.id = id
        self.tasks = []
        self.finised = 0
        self.finished_tasks = []
        self.core_start = 0

    def get_frequency(self, mode='perf'):
        if mode == 'perf':
            freq = max([task.best_freq for task in self.tasks])
        elif mode == 'energy':
            freq = min([task.best_freq for task in self.tasks])
        elif mode == 'avg':
            freq = int(np.mean([task.best_freq for task in self.tasks]))
        return freq

    def is_full(self):
        return len(self.tasks) == Constant.core_limit
    def is_empty(self):
        return len(self.tasks) == 0

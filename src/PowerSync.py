# -*- encoding: utf-8 -*-
'''
@File    :  PowerSync.py
@Time    :  2021/10/08 19:00:29
Author   :  Lu Zhang
@Version :  1.0
@Email   :  luzhang@sjtu.edu.cn
@Desc    :  None
'''
import math
from Task import Task
from Core import Core
import Constant


class PowerSync():
    def __init__(self, d_t=0, f_t=0, type='opt') -> None:
        self.type = type
        self.duration_threshold = d_t
        self.freq_threshold = f_t

    def schedule(self, workloads, step=1):
        ts = 0
        finished_tasks = []
        tasks = []
        cores = []
        workload_index = 0
        idle_cores = []
        function_queue = {}
        core_limit = Constant.core_limit

        for workload in workloads:
            function = workload[1]
            t = workload[0]
            task = Task(function, t)
            task.parse_function(Constant.path,self.type)
            task.base_init = core_limit * task.base_init
            task.base_exec = core_limit * task.base_exec
            task.real_base_exec = core_limit * task.real_base_exec

            tasks.append(task)

            if self.type == 'opt':
                best_init = task.best_init_freq
                best_exec = task.best_exec_freq

                dura_init = task.init[best_init-8]
                dura_exec = task.exec[best_exec-8]

                if self.duration_threshold == 0 and self.freq_threshold == 0:

                    key = '{},{},{},{}'.format(
                        best_init, best_exec, dura_init, dura_exec)
                    try:
                        function_queue[key].append(task)
                    except:
                        function_queue[key] = [task]
                else:
                    # consider the duration threshold:
                    add_flag = 0
                    tmp_key_freq = '{},{}'.format(best_init, best_exec)
                    tmp_key = '{},{},{},{}'.format(
                        best_init, best_exec, dura_init, dura_exec)

                    # add functions in the queue with exact power synchronization
                    for key, values in function_queue.items():
                        if tmp_key == key:
                            function_queue[key].append(task)
                            add_flag = 1
                            break

                    # add functions in the queue within threshold
                    if add_flag == 0:
                        for key, values in function_queue.items():
                            if tmp_key_freq in key:
                                f_dt = 0
                                init_sum, exec_sum = 0, 0

                                not_full_functions = len(values) % core_limit
                                if not_full_functions == 0:
                                    continue
                                else:
                                    for f in values[len(values)-not_full_functions:]:
                                        f_dura_init = f.init[f.best_init_freq-8]
                                        f_dura_exec = f.exec[f.best_exec_freq-8]
                                        init_sum += f_dura_init
                                        exec_sum += f_dura_exec
                                    init_sum += dura_init
                                    exec_sum += dura_exec
                                    init_avg = init_sum / \
                                        (not_full_functions + 1)
                                    exec_avg = exec_sum / \
                                        (not_full_functions + 1)

                                    for f in values[len(values)-not_full_functions:]:
                                        f_dura_init = f.init[f.best_init_freq-8]
                                        f_dura_exec = f.exec[f.best_exec_freq-8]
                                        init_sum = init_sum + \
                                            (f_dura_init - init_avg) ** 2
                                        exec_sum = exec_sum + \
                                            (f_dura_exec - exec_avg) ** 2
                                    init_sum = init_sum + \
                                        (dura_init - init_avg) ** 2
                                    exec_sum = exec_sum + \
                                        (dura_exec - exec_avg) ** 2
                                    f_dt = 0.5 * (math.sqrt(init_sum / ((not_full_functions+1) * init_avg * init_avg)) + math.sqrt(
                                        exec_sum / ((not_full_functions+1) * exec_avg * exec_avg)))

                                    if f_dt < self.duration_threshold:
                                        function_queue[key].append(task)
                                        add_flag = 1
                                        break
                    if add_flag == 0:
                        key = '{},{},{},{}'.format(
                            best_init, best_exec, dura_init, dura_exec)
                        try:
                            function_queue[key].append(task)
                        except:
                            function_queue[key] = [task]
                        add_flag = 1

            if self.type == 'freq2_option':
                best_init = task.best_init_freq
                best_exec = task.best_exec_freq

                key = '{},{}'.format(best_init, best_exec)
                try:
                    function_queue[key].append(task)
                except:
                    function_queue[key] = [task]

            if self.type == 'freq':
                best_init = task.best_init_freq
                best_exec = task.best_exec_freq

                key = '{},{}'.format(best_init, best_exec)
                try:
                    function_queue[key].append(task)
                except:
                    function_queue[key] = [task]

            if self.type == 'per-app':
                best_init = task.best_init_freq
                best_exec = task.best_exec_freq

                key = '{},{}'.format(best_init, best_exec)
                try:
                    function_queue[key].append(task)
                except:
                    function_queue[key] = [task]

            if self.type == 'dura':
                dura_init = task.init[4]
                dura_exec = task.exec[10]
                # dura_init = task.init[task.best_init_freq-8]
                # dura_exec = task.exec[task.best_exec_freq-8]

                key = '{},{}'.format(dura_init, dura_exec)
                try:
                    function_queue[key].append(task)
                except:
                    function_queue[key] = [task]

            if self.type == 'NPS' or self.type == 'IL':
                key = 'NPS'
                try:
                    function_queue[key].append(task)
                except:
                    function_queue[key] = [task]

        index = 0
        for tmp_tasks in function_queue.values():
            if len(tmp_tasks) < core_limit:
                core = Core(index)
                for task in tmp_tasks:
                    task.start = task.create - tmp_tasks[-1].create
                    task.coreid = index
                    core.tasks.append(task)
                cores.append(core)
                index += 1
            else:
                flag = int(len(tmp_tasks)/core_limit)
                for i in range(flag):
                    core = Core(index)
                    for task in tmp_tasks[i*core_limit:(i+1)*core_limit]:
                        task.start = task.create - \
                            tmp_tasks[(i+1)*core_limit - 1].create
                        task.coreid = index
                        core.tasks.append(task)
                    cores.append(core)
                    index += 1
                if len(tmp_tasks) % core_limit != 0:
                    core = Core(index)
                    for task in tmp_tasks[flag*core_limit:]:
                        task.start = task.create - tmp_tasks[-1].create
                        task.coreid = index
                        core.tasks.append(task)
                    cores.append(core)
                    index += 1

        while True:
            ts += step
            for i in range(len(cores)):
                core = cores[i]
                tmp_core = Core(i)
                freq = 0
                flag = 0
                if not core.is_empty():
                    if self.type == 'RR-P':
                        freq = 22
                    else:
                        freq = core.get_frequency('avg')
                for task in core.tasks:
                    if task.last_freq == 0:
                        task.last_freq = freq
                    # if freq != task.best_freq:
                    if freq != task.true_best_freq: # for per-app
                        task.not_best_freq = task.not_best_freq + 1
                    task.freq.append(task.last_freq)
                    if flag == 0:
                        for tmp_task in core.finished_tasks:
                            tmp_task.finished_freqs.append(task.last_freq)
                            tmp_task.finished_run = tmp_task.finished_run + 1
                            tmp_core.finished_tasks.append(tmp_task)
                        flag = 1
                    task.need_freq.append(task.best_freq)
                    if task.last_freq != freq:
                        task.last_freq = freq
                        task.adjust_num = task.adjust_num + 1
                        tmp_core.tasks.append(task)

                        continue
                    if task.init_phase:
                        duration = step * task.init_ratio[freq - 8]
                    else:
                        duration = step * task.exec_ratio[freq - 8]
                    task.duration += duration

                    if task.init_phase and task.duration > task.base_init:
                        task.init_phase = False
                        task.best_freq = task.best_exec_freq
                        task.true_best_freq = task.true_best_exec_freq

                    # if self.type == 'freq2_option':
                    #     tmp_core.tasks.append(task)
                    #     if task.end == 0 and task.duration >= task.base_init + task.base_exec:
                    #     # complete
                    #         task.end = ts
                    #         task.best_freq = 0
                    #         task.last_freq = 0
                    #         tmp_core.finised += 1
                    #         finished_tasks.append(task)
                    if task.duration < task.base_init + task.real_base_exec:
                        ## not complete
                        tmp_core.tasks.append(task)
                    if task.duration >= task.base_init + task.real_base_exec:
                        # complete
                        task.end = ts
                        finished_tasks.append(task)
                        # if self.type == 'freq2_option':
                        tmp_core.finished_tasks.append(task)
                cores[i] = tmp_core
                if len(tmp_core.tasks) == 0:
                    # idle core
                    idle_cores.append(i)
            if len(tasks) == len(finished_tasks):
                break
        self.finished = finished_tasks
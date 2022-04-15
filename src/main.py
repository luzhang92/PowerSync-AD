# -*- encoding: utf-8 -*-
'''
@File    :  simulator.py
@Time    :  2021/10/08 23:42:44
Author   :  Lu Zhang
@Version :  1.0
@Email   :  luzhang@sjtu.edu.cn
@Desc    :  None
'''

import numpy as np
from PowerSync import PowerSync
from workload import workload_generator

from Task import Task
from Core import Core
import Constant
import argparse
import json


def analyze(finished_tasks, step=1):

    results = {'statistics':{}, 'details':{}}

    latencys = []
    energys = []
    durations = []
    edps = []

    power = [0.513948276, 0.676344828, 0.675396552, 0.81912069, 0.843741379, 0.900465517, 0.960103448,
             1.162258621, 1.191, 1.421413793, 1.456827586, 1.609741379, 1.710310345, 1.763568966, 1.866051724]
    
    functions_detail = {}

    for task in finished_tasks:
        latency = task.end - task.start
        # duration = task.end - task.create
        duration = task.end
        energy = 0
        for freq in task.freq:
            energy = energy + step * power[freq-8] / Constant.core_limit
        for freq in task.finished_freqs:
            energy = energy + step * power[freq-8] /Constant.core_limit
        edp = duration * energy

        latencys.append(latency)
        energys.append(energy)
        durations.append(duration)
        edps.append(edp)

        f_name = task.name
        if f_name not in functions_detail.keys():
            functions_detail[f_name] = {}

        finish_async_ratio = task.finished_run / (len(task.freq)+len(task.finished_freqs))

        try:
            # functions_detail[f_name]['freq'].append(task.freq) #list
            # functions_detail[f_name]['need_freq'].append(task.need_freq)
            functions_detail[f_name]['adjust_num'].append(task.adjust_num)
            functions_detail[f_name]['latency'].append(latency)
            functions_detail[f_name]['duration'].append(duration)
            functions_detail[f_name]['edp'].append(edp)
            functions_detail[f_name]['not_best'].append(task.not_best_freq)
            functions_detail[f_name]['finish_async'].append(finish_async_ratio)
        except:
            # functions_detail[f_name]['freq']=[task.freq] #list
            # functions_detail[f_name]['need_freq']=[task.need_freq]
            functions_detail[f_name]['adjust_num']=[task.adjust_num]
            functions_detail[f_name]['latency'] = [latency]
            functions_detail[f_name]['duration'] = [duration]
            functions_detail[f_name]['edp'] = [edp]
            functions_detail[f_name]['not_best']=[task.not_best_freq]
            functions_detail[f_name]['finish_async']=[finish_async_ratio]

    latency_avg = np.mean(latencys)
    latency_50 = np.percentile(latencys, 50)
    latency_90 = np.percentile(latencys, 90)
    latency_99 = np.percentile(latencys, 99)

    energy_avg = np.mean(energys)
    duration_avg = np.mean(durations)
    edps_avg = np.mean(edps)

    statistics_data = {'latency_avg':latency_avg,'latency_50':latency_50,'latency_90':latency_90,'latency_99':latency_99,'energy_avg':energy_avg,'duration_avg':duration_avg,'edps_avg':edps_avg}

    results['details'] = functions_detail
    results['statistics'] = statistics_data
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameters to this script')
    parser.add_argument('--s', type=str, default='NPS',
                        help='the scheme of this script: RR, opt, freq1, freq2, dura')
    parser.add_argument('--t', type=str, default='plain', help='the trace of workloads:place, azure, ali')
    parser.add_argument('--d', type=str, default='uniform',
                        help='the workload distribution: uniform, possion')
    parser.add_argument('--w', type=str, default='MHo',
                        help='the workloads: MHo, Ho1, Ho2, He')
    # parser.add_argument('--m', type=str, default='perf',
    #                     help="the mode of RR: perf, energy; the mode of PS: freq, whole, opt")
    parser.add_argument('--f', type=str, default='alugo', help='functions')
    parser.add_argument('--dt', type=float, default=0,
                        help='the duration threshold')
    parser.add_argument('--ft', type=float, default=0,
                        help='frequency threshold')
    parser.add_argument('--duration', type=int, default=1000,
                        help='the duration of the invocation (ms)')
    parser.add_argument('--r', type=int, default=1,
                        help='the rate of function per 1s (ms)')
    parser.add_argument('--seed', type=int, default=1,
                        help='the seed for random')
    args = parser.parse_args()

    Wg = workload_generator(args.w)
    if args.d == 'uniform':
        workloads = Wg.workload_uniform(args.t, args.duration, args.r, args.f)

    if args.d == 'possion':
        workloads = Wg.workload_possion(args.t, args.duration, args.r, args.seed, args.f)

    scheduler = PowerSync(d_t=args.dt, type=args.s)
    scheduler.schedule(workloads)
    filename = '../Results/{}_{}_{}_{}_{}_{}_{}_{}.json'.format(
        args.s, args.t, args.d, args.w, args.f, args.duration, args.r,args.dt)

    finished_tasks = scheduler.finished
    results = analyze(finished_tasks)
    with open(filename, 'w') as f:
        json.dump(results, f)

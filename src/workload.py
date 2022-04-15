# -*- encoding: utf-8 -*-
'''
@File    :  workload.py
@Time    :  2021/10/08 11:24:02
Author   :  Lu Zhang
@Version :  1.0
@Email   :  luzhang@sjtu.edu.cn
@Desc    :  Generate the workload sequence for experiment
'''
import numpy as np
import azure_trace
import ali_trace

# total functions:
# functions = ['alugo', 'alujs', 'alupy', 'aluphp', 'alurb',
#  'aluswift', 'float', 'IOpy', 'markdown2html', 'ocr', 'sentiment']
functions = ['alugo', 'alujs', 'alupy', 'aluphp',
             'aluswift', 'float', 'markdown2html', 'sentiment']
functions_f = [function+'-f' for function in functions]

functions_d = [functions[i]+'-d' for i in range(len(functions)-1)]

total_functions = functions + functions_f + functions_d


class workload_generator():
    def __init__(self, type) -> None:
        # type MHo, Ho1, Ho2, He
        self.type = type

    # Generate load
    def workload_uniform(self, trace, duration, rate, function='alugo'):
        # uniform 20ms, 1h
        workload = []
        if trace == 'plain':
            interval = int(1000 / rate)
            if self.type == 'MHo':
                # most homogeneous
                for t in range(0, duration, interval):
                    workload.append((t, function))

            if self.type == 'SPF':
                index = 0
                for t in range(0, duration, interval):
                    if index % 2 == 0:
                        workload.append((t, function))
                    else:
                        workload.append((t, function+'-f'))
                    index += 1

            if self.type == 'SPD':  # no sentiment
                index = 0
                for t in range(0, duration, interval):
                    if index % 2 == 0:
                        workload.append((t, function))
                    else:
                        workload.append((t, function+'-d'))
                    index += 1
            if self.type == 'ASP':
                ts = range(0, duration, interval)
                functions_num = len(total_functions)
                for i in range(len(ts)):
                    workload.append(
                        (ts[i], total_functions[i % functions_num]))

        if trace == 'azure':
            trace_d = azure_trace.trace
            duration_s = int(duration/1000)
            step = int(len(trace_d)/duration_s)

            trace_choose = [trace_d[i]
                            for i in range(0, step*duration_s, step)]

            trace_mean = np.mean(trace_choose)
            scale_ratio = rate/trace_mean

            trace_rates = [round(t*scale_ratio) for t in trace_choose]

            if self.type == 'MHo':
                for i in range(len(trace_rates)):
                    trace_rate = trace_rates[i]
                    interval = int(round(1000/trace_rate))
                    for t in range(i*1000, (i+1)*1000, interval):
                        workload.append((t, function))
            if self.type == 'SPF':
                index = 0
                for i in range(len(trace_rates)):
                    trace_rate = trace_rates[i]
                    interval = int(round(1000/trace_rate))
                    for t in range(i*1000, (i+1)*1000, interval):
                        if index % 2 == 0:
                            workload.append((t, function))
                        else:
                            workload.append((t, function+'-f'))
                        index += 1

            if self.type == 'SPD':
                index = 0
                for i in range(len(trace_rates)):
                    trace_rate = trace_rates[i]
                    interval = int(round(1000/trace_rate))
                    for t in range(i*1000, (i+1)*1000, interval):
                        if index % 2 == 0:
                            workload.append((t, function))
                        else:
                            workload.append((t, function+'-d'))
                        index += 1

            if self.type == 'ASP':
                index = 0
                functions_num = len(total_functions)
                for i in range(len(trace_rates)):
                    trace_rate = trace_rates[i]
                    interval = int(round(1000/trace_rate))
                    for t in range(i*1000, (i+1)*1000, interval):
                        workload.append(
                            (t, total_functions[index % functions_num]))
                        index += 1

        if trace == 'ali':
            trace_d = ali_trace.trace
            duration_s = int(duration/1000)
            step = int(len(trace_d)/duration_s)

            trace_choose = [trace_d[i]
                            for i in range(0, step*duration_s, step)]

            trace_mean = np.mean(trace_choose)
            scale_ratio = rate/trace_mean

            trace_rates = [round(t*scale_ratio) for t in trace_choose]

            if self.type == 'MHo':
                for i in range(len(trace_rates)):
                    trace_rate = trace_rates[i]
                    interval = int(round(1000/trace_rate))
                    for t in range(i*1000, (i+1)*1000, interval):
                        workload.append((t, function))
            if self.type == 'SPF':
                index = 0
                for i in range(len(trace_rates)):
                    trace_rate = trace_rates[i]
                    interval = int(round(1000/trace_rate))
                    for t in range(i*1000, (i+1)*1000, interval):
                        if index % 2 == 0:
                            workload.append((t, function))
                        else:
                            workload.append((t, function+'-f'))
                        index += 1

            if self.type == 'SPD':
                index = 0
                for i in range(len(trace_rates)):
                    trace_rate = trace_rates[i]
                    interval = int(round(1000/trace_rate))
                    for t in range(i*1000, (i+1)*1000, interval):
                        if index % 2 == 0:
                            workload.append((t, function))
                        else:
                            workload.append((t, function+'-d'))
                        index += 1

            if self.type == 'ASP':
                index = 0
                functions_num = len(total_functions)
                for i in range(len(trace_rates)):
                    trace_rate = trace_rates[i]
                    interval = int(round(1000/trace_rate))
                    for t in range(i*1000, (i+1)*1000, interval):
                        workload.append(
                            (t, total_functions[index % functions_num]))
                        index += 1

        return workload
        # possion

    def workload_possion(self, trace, duration, rate, seed=1, function='alugo'):
        np.random.seed(seed)
        workload = []
        if trace == 'plain':
            beta = 1.0/rate
            inter_arrivals = list(np.random.exponential(
                scale=beta, size=int(1.5*duration*rate/10)))

            if self.type == 'MHo':
                t = 0
                for i in range(int(duration*rate/10)):
                    workload.append((int(t), function))
                    t += inter_arrivals[i]*10

            if self.type == 'SPF':
                t = 0
                index = 0
                for i in range(int(duration*rate/10)):
                    if i % 2 == 0:
                        workload.append((int(t), function))
                    else:
                        workload.append((int(t), function+'-f'))
                    index += 1
                    t += inter_arrivals[i]*10

            if self.type == 'SPD':  
                t = 0
                index = 0
                for i in range(int(duration*rate/10)):
                    if i % 2 == 0:
                        workload.append((int(t), function))
                    else:
                        workload.append((int(t), function+'-d'))
                    index += 1
                    t += inter_arrivals[i]*10

            if self.type == 'ASP':
                t = 0
                functions_num = len(total_functions)
                for i in range(int(duration*rate/10)):
                    workload.append(
                        (int(t), total_functions[i % functions_num]))
                    t += inter_arrivals[i]*10

        if trace == 'azure':
            trace_d = azure_trace.trace
            duration_s = int(duration/10)
            step = int(len(trace_d)/duration_s)

            trace_choose = [trace_d[i]
                            for i in range(0, step*duration_s, step)]

            trace_mean = np.mean(trace_choose)
            scale_ratio = rate/trace_mean

            trace_rates = [round(t*scale_ratio) for t in trace_choose]

            if self.type == 'MHo':
                t = 0
                for i in range(len(trace_rates)):
                    trace_rate = int(trace_rates[i])
                    beta = 1.0/trace_rate
                    inter_arrivals = list(np.random.exponential(
                        scale=beta, size=int(1.5*trace_rate)))
                    for j in range(trace_rate):
                        workload.append((int(t), function))
                        t += inter_arrivals[j]*10

            if self.type == 'SPF':
                t = 0
                index = 0
                for i in range(len(trace_rates)):
                    trace_rate = int(trace_rates[i])
                    beta = 1.0/trace_rate
                    inter_arrivals = list(np.random.exponential(
                        scale=beta, size=int(1.5*trace_rate)))
                    for j in range(trace_rate):
                        if index % 2 == 0:
                            workload.append((int(t), function))
                        else:
                            workload.append((int(t), function+'-f'))

                        index += 1
                        t += inter_arrivals[j]*10

            if self.type == 'SPD':
                t = 0
                index = 0
                for i in range(len(trace_rates)):
                    trace_rate = int(trace_rates[i])
                    beta = 1.0/trace_rate
                    inter_arrivals = list(np.random.exponential(
                        scale=beta, size=int(1.5*trace_rate)))
                    for j in range(trace_rate):
                        if index % 2 == 0:
                            workload.append((int(t), function))
                        else:
                            workload.append((int(t), function+'-d'))

                        index += 1
                        t += inter_arrivals[j]*10

            if self.type == 'ASP':
                t = 0
                functions_num = len(total_functions)
                index = 0
                for i in range(len(trace_rates)):
                    trace_rate = int(trace_rates[i])
                    beta = 1.0/trace_rate
                    inter_arrivals = list(np.random.exponential(
                        scale=beta, size=int(1.5*trace_rate)))
                    for j in range(trace_rate):
                        workload.append(
                            (int(t), total_functions[index % functions_num]))
                        t += inter_arrivals[j]*10
                        index += 1

        if trace == 'ali':
            trace_d = ali_trace.trace
            duration_s = int(duration/10)
            step = int(len(trace_d)/duration_s)

            trace_choose = [trace_d[i]
                            for i in range(0, step*duration_s, step)]

            trace_mean = np.mean(trace_choose)
            scale_ratio = rate/trace_mean

            trace_rates = [round(t*scale_ratio) for t in trace_choose]

            if self.type == 'MHo':
                t = 0
                for i in range(len(trace_rates)):
                    trace_rate = int(trace_rates[i])
                    beta = 1.0/trace_rate
                    inter_arrivals = list(np.random.exponential(
                        scale=beta, size=int(1.5*trace_rate)))
                    for j in range(trace_rate):
                        workload.append((int(t), function))
                        t += inter_arrivals[j]*10

            if self.type == 'SPF':
                t = 0
                index = 0
                for i in range(len(trace_rates)):
                    trace_rate = int(trace_rates[i])
                    beta = 1.0/trace_rate
                    inter_arrivals = list(np.random.exponential(
                        scale=beta, size=int(1.5*trace_rate)))
                    for j in range(trace_rate):
                        if index % 2 == 0:
                            workload.append((int(t), function))
                        else:
                            workload.append((int(t), function+'-f'))

                        index += 1
                        t += inter_arrivals[j]*10

            if self.type == 'SPD':
                t = 0
                index = 0
                for i in range(len(trace_rates)):
                    trace_rate = int(trace_rates[i])
                    beta = 1.0/trace_rate
                    inter_arrivals = list(np.random.exponential(
                        scale=beta, size=int(1.5*trace_rate)))
                    for j in range(trace_rate):
                        if index % 2 == 0:
                            workload.append((int(t), function))
                        else:
                            workload.append((int(t), function+'-d'))

                        index += 1
                        t += inter_arrivals[j]*10

            if self.type == 'ASP':
                t = 0
                functions_num = len(total_functions)
                index = 0
                for i in range(len(trace_rates)):
                    trace_rate = int(trace_rates[i])
                    beta = 1.0/trace_rate
                    inter_arrivals = list(np.random.exponential(
                        scale=beta, size=int(1.5*trace_rate)))
                    for j in range(trace_rate):
                        workload.append(
                            (int(t), total_functions[index % functions_num]))
                        t += inter_arrivals[j]*10
                        index += 1

        return workload


# test

if __name__ == '__main__':
    Wg = workload_generator('SPF')

    # def workload_uniform(self, trace, duration, rate, function='alugo'):
    workload = Wg.workload_possion('ali', 1000, 10, 1, 'alugo')
    print(len(workload))
    # workload = Wg.workload_uniform('ali',10000, 20,'alugo')

    print(workload)

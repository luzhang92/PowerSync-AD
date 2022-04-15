import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

functions = ['alugo', 'alujs', 'alupy', 'aluphp', 'alurb','aluswift', 'float', 'IOpy', 'markdown2html', 'ocr', 'sentiment']
# functions = ['alugo', 'alujs', 'alupy', 'aluphp', 'aluswift', 'float', 'IOpy', 'markdown2html', 'ocr', 'sentiment']

functions_f = [function+'-f' for function in functions]
functions_d = [functions[i]+'-d' for i in range(len(functions)-1)]

rates = [10]
# rates=[20]
# modes = ['RR','freq2','dura','opt']
modes = ['NPS','IL','per-app','freq','dura','opt']
# modes=['opt']
# distributions = ['uniform','possion']
distributions=['possion']
workloads = ['SPF','SPD']
# workloads = ['MHo']
traces = ['plain','azure','ali']
# traces = ['ali']

baseline = {}
for trace in traces:
    baseline[trace] = {}
    for rate in rates:
        baseline[trace][rate] = {}
        for distribution in distributions:
            baseline[trace][rate][distribution] = {}
            for workload in workloads:
                baseline[trace][rate][distribution][workload] = {}
                for function in functions:
                    filename = '../Results/{}_{}_{}_{}_{}_{}_{}_{}.json'.format('NPS',trace,distribution,workload,function,1000, rate,0)

                    with open(filename,'r') as f:
                        result = json.load(f)
                        detailed = result['details']

                    for key,value in detailed.items():
                        baseline[trace][rate][distribution][workload][key]={}
                        latency = np.mean(value['latency'])
                        baseline[trace][rate][distribution][workload][key]['latency'] = latency
                        duration = np.mean(value['duration'])
                        baseline[trace][rate][distribution][workload][key]['duration'] = duration
                        
                        baseline[trace][rate][distribution][workload][key]['wait_time'] = latency-duration

                        edp = np.mean(value['edp'])
                        baseline[trace][rate][distribution][workload][key]['edp'] = edp
                        energy = np.mean([value['edp'][i]/value['duration'][i] for i in range(len(value['edp']))])
                        baseline[trace][rate][distribution][workload][key]['energy'] = energy

                # baseline[rate][distribution][workload][function]

for trace in traces:
    for rate in rates:
        for distribution in distributions:
            for workload in workloads:
                data = {'norm_latency':{},'norm_energy':{},'norm_edp':{}}
                for mode in modes:
                    norm_latencys = []
                    norm_energys = []
                    norm_edps = []
                    for function in functions:
                        filename = '../Results/{}_{}_{}_{}_{}_{}_{}_{}.json'.format(mode,trace,distribution,workload,function,1000, rate,0)

                        with open(filename, 'r') as f:
                            result = json.load(f)
                            detailed = result['details']

                        for key,value in detailed.items():
                            latency = np.mean(value['latency'])
                            latency_base = baseline[trace][rate][distribution][workload][key]['latency']
                            norm_latencys.append(latency/latency_base)

                            edp = np.mean(value['edp'])
                            base_edp = baseline[trace][rate][distribution][workload][key]['edp']
                            norm_edps.append(edp/base_edp)

                            energy = np.mean([value['edp'][i]/value['duration'][i] for i in range(len(value['edp']))])
                            base_energy = baseline[trace][rate][distribution][workload][key]['energy']
                            norm_energys.append(energy/base_energy)

                    data['norm_latency'][mode] = np.mean(norm_latencys)
                    data['norm_energy'][mode] = np.mean(norm_energys)
                    data['norm_edp'][mode] = np.mean(norm_edps)
                
                df = pd.DataFrame(data)
                filename = './effectiveness_csv/{}_{}_{}_{}_{}.csv'.format(trace,distribution,workload,10000,rate)
                df.to_csv(filename)


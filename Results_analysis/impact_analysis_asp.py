import pandas as pd
import numpy as np
import json

rates = [10]
# rates=[20]
modes = ['NPS','IL','per-app','freq','dura','opt']
# modes=['opt']
distributions = ['possion']
# distributions=['uniform']
workloads = ['ASP']
# workloads = ['MHo']
# traces = ['plain','azure','ali']
traces = ['plain','azure','ali']
functions=['alugo']


for trace in traces:
    for rate in rates:
        for distribution in distributions:
            for workload in workloads:
                data = {'adjust_num':{},'BFV':{},'finish_async':{}}
                for mode in modes:
                    adjust_nums = []
                    not_bests = []
                    finish_async_ratios = []
                    for function in functions:
                        filename = '../Results/{}_{}_{}_{}_{}_{}_{}_{}.json'.format(mode,trace,distribution,workload,function,1000, rate,0)
                        with open(filename, 'r') as f:
                            result = json.load(f)
                            detailed = result['details']

                        for key,value in detailed.items():
                            
                            adjust_num = np.mean(value['adjust_num'])
                            adjust_nums.append(adjust_num)

                            not_best = np.mean([value['not_best'][i]/value['duration'][i] for i in range(len(value['duration']))])
                            not_bests.append(not_best)
                            
                            async_ratio = np.mean(value['finish_async'])
                            finish_async_ratios.append(async_ratio)
                            
                    data['adjust_num'][mode] = np.mean(adjust_nums)
                    data['BFV'][mode] = np.mean(not_bests)
                    data['finish_async'][mode] = np.mean(finish_async_ratios)
                
                df = pd.DataFrame(data)
                filename = './impact_csv/{}_{}_{}_{}_{}.csv'.format(trace,distribution,workload,10000,rate)
                df.to_csv(filename)


# PowerSync
This repo is for **PowerSync**, a synchronization-based power management framework that ensures the optimal efficiency based on a clear understanding of functions.

## What is PowerSync
PowerSync is a novel power management framework which provides high power efficiency when functions co-locate on the same processor core. Specifically, PowerSync adopts a two-pronged strategy when performing power synchronization. First, \powersync{} could accurately estimate the optimal operational settings of various functions including its best-suited frequency and duration in different phases. It synchronizes the power management of various functions by deploying functions with the same optimal operational setting on the same processor core. Additionally, PowerSync has a built-in frequency/phase cooperative switch mechanism which is able to restore the best-suited frequency of functions with low overhead as their phases move forward. 

## Running
### Preparing Python environment

`
$ pip install -r requirements.txt
`

### Getting Start
1. Run different algorithm

    `
    $ cd utils/
    `
    
    1.1 Run NPS with SPF and SPD function pools:

    `
    $ bash run_NPS.sh
    `

    1.2 Run IL with SPF and SPD function pools:
    
    `
    $ bash run_IL.sh
    `

    1.3 Run Per-APP with SPF and SPD function pools:
    
    `
    $ bash run_per-app.sh
    `

    1.4 Run PS&Freq with SPF and SPD function pools:
    
    `
    $ bash run_freq.sh
    `

    1.5 Run PS&Dura with SPF and SPD function pools:
    
    `
    $ bash run_dura.sh
    `

    1.6 Run PS&Opt with SPF and SPD function pools:
    
    `
    $ bash run_opt.sh
    `
2. Analyze the results of different schemes

    After running different schemes, the results are stored in the file Results. Next, we will analyze the raw data.

    `
    $ cd Results_analysis/
    `

    2.1 Analyze the effectiveness of PowerSync

    `
    $ python effectiveness_analysis_spf_spd.py
    `

    `
    $ python effectiveness_analysis_asp.py
    `

    The results are stored in the file effectiveness_csv. The results include the normalized latency, energy and edp of different schemes.

    2.2 Analyze the impact factor of PowerSync

    `
    $ python impact_analysis_spf_spd.py
    `

    `
    $ python impact_analysis_asp.py
    `

    The results are stored in the file impact_csv. The results include the BFV ration, finish_async ratio of different schemes.

## Running with Docker

You can use the command

`
$ docker run -ti luke92/powersync:AD /bin/bash
`

`
$ cd /home/PowerSync-AD/
`

Then you can run the code as above.
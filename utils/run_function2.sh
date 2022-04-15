#! /bin/bash
duration=$1
rate=$2
dis=$3
trace=$4
workload=$5
for function in 'alugo' 'alujs' 'alupy' 'aluphp' 'alurb' 'aluswift' 'float' 'IOpy' 'markdown2html' 'ocr' 'sentiment'
do
    for s in 'RR' 'freq2' 'dura' 'opt'
    do
        python ../src/simulator.py --s $s --w $workload --t $trace --d $dis --f $function --duration $duration --r $rate &
        #python simulator.py --m $mode --d possion --f $function --duration 60000 --r 1000 &
    done
done

# for function in 'alugo' 'alujs' 'alupy' 'aluphp' 'alurb' 'aluswift' 'float' 'IOpy' 'markdown2html' 'ocr' 'sentiment'
# do
#     for mode in 'opt' 'freq1' 'freq2' 'dura'
#     do
#         # python simulator.py --s PS --m $mode --f $function --duration 60000 --r 100 &
#         python ../src/simulator.py --s PS --m $mode --d $dis --f $function --duration $duration --r $rate &
#     done
# done
echo $dis $duration $rate is "done"
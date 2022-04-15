for trace in 'azure' 'ali' 'plain'
# for trace in 'plain'
do
    for dis in 'possion'
    do
        for rate in 10
        do
            for s in 'per-app'
            do
                for function in 'alugo' 'alujs' 'alupy' 'aluphp' 'alurb' 'aluswift' 'float' 'IOpy' 'markdown2html' 'ocr' 'sentiment'
                do
                    for workload in 'SPF' 'SPD'
                    do
                        python ../src/main.py --s $s --t $trace --d $dis --duration 1000 --r $rate --w $workload --f $function &
                    done
                done
            done
        done
    done
done
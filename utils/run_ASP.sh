for trace in 'azure' 'ali' 'plain'
do
    for dis in 'possion'
    do
        for rate in 10
        do
            for s in 'NPS' 'IL' 'dura' 'freq' 'opt' 'per-app'
            do
                python ../src/main.py --s $s --t $trace --d $dis --duration 1000 --r $rate --w ASP &
            done
        done
    done
done
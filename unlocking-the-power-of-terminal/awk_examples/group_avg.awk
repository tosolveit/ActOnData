#!/usr/bin/awk -f
# AWK script to calculate the sum and average by group

{
    sum[$6] += $7;
    count[$6]++;
}

END {
    for (group in sum) {
        print group, sum[group], sum[group] / count[group];
    }
}


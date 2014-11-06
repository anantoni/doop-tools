#!/bin/bash
#
# The intended way to run this script is something like the following:
#
# $0 a2a doop-latest/collect/*.bach-default
#
# or like this, for the sake of human readability:
#
# $0 -h a2a doop-latest/collect/*.bach-default


if [[ $1 = -h ]]; then
    # Redirect stdout ( > ) into a named pipe ( >() ) running "column"
    exec > >(column -t -s \;)
    shift
fi

case $1 in
    "a2a")
        edges="Application ===> Application";;
    "a2l")
        edges="Application ===> Library";;
    "l2a")
        edges="Library ===> Application";;
    "l2l")
        edges="Library ===> Library";;
    *)
        echo "Usage: $0 [-h] [a2a|a2l|l2a|l2l] FILES" >&2; exit 1;;
esac
shift

files="$@"

# List of all DaCapo bach benchmarks
benchmarks="avrora batik eclipse h2 jython luindex lusearch pmd sunflow xalan"
declare -A benchmap


echo -n -e "Benchmarks;"
for benchmark in $benchmarks; do
    echo -n -e "$benchmark;"
    for file in $files; do
        if [[ $file = *${benchmark}* ]]; then
            benchmap[$benchmark]="$file"
        fi
    done
done
echo

echo -n -e "Total Static Edges;"
for benchmark in $benchmarks; do
    file="${benchmap[$benchmark]}"
    if [[ -z $file ]]; then
        echo -e -n "n/a;"
        continue
    fi
    lines=$(grep "$edges" $file -B 3 -A 2 | tail -n 1 | awk -F: '{print $2}' | tr -d " ")
    echo -e -n "${lines};"
done
echo

echo -n -e "Total Dynamic Edges;"
for benchmark in $benchmarks; do
    file="${benchmap[$benchmark]}"
    if [[ -z $file ]]; then
        echo -e -n "n/a;"
        continue
    fi
    lines=$(grep "$edges" $file -B 3 -A 3 | tail -n 1 | awk -F: '{print $2}' | tr -d " ")
    echo -e -n "${lines};"
done
echo

for i in $(seq 1 7); do
    echo -n -e "Dynamic Edges $i/7;"
    for benchmark in $benchmarks; do
        file="${benchmap[$benchmark]}"
        if [[ -z $file ]]; then
            echo -e -n "n/a;"
            continue
        fi
        lines=$(grep "$edges" $file -B 3 -A 4 -m $i | tail -n 1 | awk -F: '{print $2}' | tr -d " ")
        echo -e -n "${lines};"
    done
    echo
done

echo -n -e "Execution Times;"
for benchmark in $benchmarks; do
    file="${benchmap[$benchmark]}"
    if [[ -z $file ]]; then
        echo -e -n "n/a;"
        continue
    fi

    # Determine the location of the log file
    filedir=`dirname $file`
    filebase=`basename $file`
    logfile=`echo $filedir/.logs/$filebase*`

    lines=$(grep "MBBENCH logicblox START" $logfile -A 1 | tail -n 1 | awk -F: '{print $2}' | tr -d " ")
    echo -e -n "${lines};"
done
echo

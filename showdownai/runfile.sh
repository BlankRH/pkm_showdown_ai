#!/bin/sh
#echo ls ./epsilonnn/BaselineAgent/wins | grep '.log' | wc -l;
cnt=0
while ((cnt<20)); do
    let "cnt+=1"
    python showdown.py --username='epsilonnn' --password='python' --agent='BaselineAgent'
done
cnt2=0
while ((cnt2<20)); do
    let "cnt2+=1"
    python showdown.py --username='hubbbb' --password='VouchSuperBohos+2' --agent='MinimaxAgent'
done

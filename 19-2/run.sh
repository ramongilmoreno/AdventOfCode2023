#!/bin/bash

f () { echo $1; cat ../19-1/$1 | python3 parse.py | sed "s/^/    /g"; }
f example.txt
echo "Not fast enough for input.txt"
exit -1
f input.txt

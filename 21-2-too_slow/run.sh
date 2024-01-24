#!/bin/bash

f () { echo $1; cat ../21-1/$1 | python3 parse.py | sed "s/^/    /g"; }
f example.txt
exit -1
f input.txt

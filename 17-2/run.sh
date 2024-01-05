#!/bin/bash

f () { echo $1; cat ../17-1/$1 | python3 parse.py | sed "s/^/    /g"; }
f ../17-2/example2.txt
f example.txt
f input.txt

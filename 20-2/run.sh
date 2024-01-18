#!/bin/bash

f () { echo $1; cat ../20-1/$1 | python3 parse.py | sed "s/^/    /g"; }
f input.txt

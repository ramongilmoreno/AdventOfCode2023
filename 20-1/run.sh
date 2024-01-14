#!/bin/bash

f () { echo $1; cat $1 | python3 parse.py | sed "s/^/    /g"; }
f example1.txt
f example2.txt
f input.txt

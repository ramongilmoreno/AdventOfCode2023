#!/bin/bash

f () { echo $1; cat $1 | python3 parse.py | sed "s/^/    /g"; }
time f ../12-1/example.txt
time f ../12-1/input.txt

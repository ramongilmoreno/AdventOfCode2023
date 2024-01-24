#!/bin/bash

f () { echo $1; cat ../21-1/$1 | python3 parse.py | sed "s/^/    /g"; }
time f example.txt
time f input.txt

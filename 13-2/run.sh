#!/bin/bash

f () { echo $1; cat ../13-1/$1 | python3 parse.py | sed "s/^/    /g"; }
f example.txt
f input.txt

#!/bin/bash

f () { cat $1 | awk -f ../11-1/parse.awk -v expansion=2 | sed "s/^/    /g"; }
echo Example
f ../11-1/example.txt
echo Input
f ../11-1/input.txt 

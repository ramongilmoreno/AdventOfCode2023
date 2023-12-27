#!/bin/bash

f () { cat $1 | awk -f parse.awk -v expansion=$2 | sed "s/^/    /g"; }
echo Example with 2
f ../11-1/example.txt 2
echo Example with 10
f ../11-1/example.txt 10
echo Example with 100
f ../11-1/example.txt 100
echo Input
f ../11-1/input.txt 1000000

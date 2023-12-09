#!/bin/bash

f () { (head -1 $1 | sed "s/././g"; cat $1; head -1 $1 | sed "s/././g") | sed "s/.*/..&../g" | awk -f parse.awk |sed "s/^/    /g"; }

echo Example
f ../03-1/example.txt
echo Input
f ../03-1/input.txt

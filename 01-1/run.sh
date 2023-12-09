#!/bin/bash

run () { cat $1 | ./sum.sh | sed "s/^/    /g"; }
echo Example
run example.txt

echo Input
run input.txt

#!/bin/bash

run () { ./sum.sh | sed "s/^/    /g"; }

echo Example
cat example.txt | run

echo Input
cat ../01-1/input.txt | run

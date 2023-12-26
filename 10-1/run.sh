#!/bin/bash

f () { python3 parse.py | sed "s/^/    /g"; }
echo Example 1
cat example1.txt | f
echo Example 2
cat example2.txt | f
echo Input
cat input.txt | f

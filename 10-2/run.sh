#!/bin/bash

f () { python3 parse.py | sed "s/^/    /g"; }
echo Example 1
cat example1.txt | f
echo Example 2
cat example2.txt | f
echo Example 3
cat example3.txt | f
echo Input
cat ../10-1/input.txt | f

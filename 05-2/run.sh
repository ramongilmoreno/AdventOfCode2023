#!/bin/bash

f () { python3 parse.py | sed "s/^/    /g"; }
echo Example
cat ../05-1/example.txt | f
echo Input
cat ../05-1/input.txt | f

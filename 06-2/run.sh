#!/bin/bash

f () { python3 parse.py | sed "s/^/    /g"; }
echo Example
cat ../06-1/example.txt | f
echo Input
cat ../06-1/input.txt | f

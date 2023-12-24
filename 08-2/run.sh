#!/bin/bash

f () { python3 parse.py | sed "s/^/    /g"; }
echo Example
cat example.txt | f
echo Input
cat ../08-1/input.txt | f

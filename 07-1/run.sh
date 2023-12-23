#!/bin/bash

f () { python3 parse.py 2> /dev/null | sed "s/^/    /g" | tail -30; }
echo Example
cat example.txt | f
echo Input
cat input.txt | f

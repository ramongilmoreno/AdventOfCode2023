#!/bin/bash

# Just reverse the words in the input, and it is the same problem as 09-1
reverse () { awk '{ for (i = NF; i > 0; i--) { printf("%s ",$i) }; printf("\n")}'; }

f () { reverse | python3 ../09-1/parse.py | sed "s/^/    /g"; }
echo Example
cat ../09-1/example.txt | f
echo Input
cat ../09-1/input.txt | f

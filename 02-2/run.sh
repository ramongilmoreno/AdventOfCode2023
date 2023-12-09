#!/bin/bash

f () { awk -f parse.awk | sed "s/^/    /g"; }

echo Example
cat ../02-01/example.txt | f
echo Input
cat ../02-01/input.txt | f

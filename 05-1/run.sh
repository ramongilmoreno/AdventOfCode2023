#!/bin/bash

f () { awk -f parse.awk | sed "s/^/    /g"; }
echo Example
cat example.txt | f
echo Input
cat input.txt | f

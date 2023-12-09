#!/bin/bash

f () { awk -f parse.awk | sed "s/^/    /g"; }
echo Example
cat ../04-1/example.txt | f
echo Input
cat ../04-1/input.txt | f

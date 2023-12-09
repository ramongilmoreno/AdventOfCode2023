#!/bin/bash

declare -i ACC=0

while read i; do
  # Clean start and trailing non numbers
  CLEAN=`echo $i | sed 's/^[^0-9]*//g' | sed 's/[^0-9]*$//g'`
  # Fetch first and last character
  FIRST=`echo $CLEAN | sed 's/^\(.\).*$/\1/g'`
  LAST=`echo $CLEAN | sed 's/^.*\(.\)$/\1/g'`
  ((ACC += ${FIRST}${LAST}))
  echo -e "$i\t${FIRST}${LAST}\t${ACC}"
done

echo TOTAL ${ACC}

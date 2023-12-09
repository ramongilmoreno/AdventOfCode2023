#!/bin/bash

MATCHER="(0|1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine)"
match_first () { sed -r "s/${MATCHER}.*/\1/g"; }
match_last () { sed -r "s/.*${MATCHER}/\1/g"; }

as_digits () { sed -r -e "s/(one)/1/g" -e "s/(two)/2/g" -e "s/(three)/3/g" -e "s/(four)/4/g" -e "s/(five)/5/g" -e "s/(six)/6/g" -e "s/(seven)/7/g" -e "s/(eight)/8/g" -e "s/(nine)/9/g"; }

declare -i ACC=0

while read i; do
  # Fetch first and last character
  FIRST=`echo $i | match_first | match_last | as_digits`
  LAST=`echo $i | match_last | match_first | as_digits`
  ((ACC += ${FIRST}${LAST}))
  echo -e "$i\t${FIRST}${LAST}\t${ACC}"
done

echo TOTAL ${ACC}

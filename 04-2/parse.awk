BEGIN {
  FS = "[;: ]+"
}
{
  card = $2
  copies[card]++
  acc += copies[card]
  print "Card [" card "], copies [" copies[card] "], acc [" acc "]: " $0

  winners_count = 0
  after_winners = 0
  numbers_count = 0
  for (i = 3; i <= NF; i++) {
    if ($i == "|") {
      after_winners = 1
    } else if (!after_winners) {
      winners[winners_count++] = $i
      winners_check[$i] = 1
    } else {
      if (winners_check[$i]) {
        print "Found winner " $i
        numbers_count++
      }
    }
  }
  for (i = 0; i < winners_count; i++) {
    winners_check[winners[i]] = 0
  }
  if (numbers_count) {
    for (i = 0; i < numbers_count; i++) {
      copies[card + 1 + i] += copies[card]
    }
  }
}
END {
  print "Answer: " acc
}

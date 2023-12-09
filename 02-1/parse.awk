BEGIN {
  FS="[:;, ]+"
  max_colors["red"]=12
  max_colors["green"]=13
  max_colors["blue"]=14
  valid_acc=0
}
{
  game = $2
  for (i = 3; i <= NF; i += 2) {
    value = $(i)
    color = $(i + 1)
    # print "Line " $0
    # print "Color " color " value " value
    if (max_colors[color] < value) {
      print "Invalid game " game
      next
    }
  }
  valid_acc += game
}
END {
  print "Valid games TOTAL: " valid_acc
}

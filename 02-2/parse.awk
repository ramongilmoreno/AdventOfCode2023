function max (a, b) {
  return ((a < b) ? b : a)
}
BEGIN {
  FS="[:;, ]+"
  max_colors["red"]=12
  max_colors["green"]=13
  max_colors["blue"]=14
  power_acc=0
}
{
  game = $2
  max_colors["red"]=0
  max_colors["green"]=0
  max_colors["blue"]=0
  for (i = 3; i <= NF; i += 2) {
    value = $(i)
    color = $(i + 1)
    max_colors[color] = max(value, max_colors[color])
  }
  power = max_colors["red"] * max_colors["green"] * max_colors["blue"]
  print "Power of game " game " is "  power
  power_acc += power
}
END {
  print "Power TOTAL: " power_acc
}

BEGIN {
  FS = ""
}

function push_numbers (position) {
  n = ""
  n_near = 0
  ratios_count = 0
  for (j = -1; j <= 1; j++) {
    for (k = 2; k <= (NF - 1); k++) {
      c2 = get_char(k, j)
      if (c2 ~ /[0-9]/) {
        n = n c2
        if (!n_near) {
          n_near = ((k == position - 1) || (k == position) || (k == position + 1))
        }
      } else {
        if (n_near) {
          print "Found ratio " n
          ratios[ratios_count++] = n
        }
        n = ""
        n_near = 0
      }
    }
  }
}
function get_char(pos, line_num) {
 return substr(line[line_num], pos, 1)
}
function logger (s) {
  # print s
}
{
  if (!line[0]) { line[0] = $0 }
  if (!line[1]) { line[1] = $0 }
  line[-1] = line[0]
  line[0] = line[1]
  line[1] = $0

  logger("----")
  logger(line[-1])
  logger(line[0])
  logger(line[1])

  for (i = 2; i <= (NF - 1); i++) {
    logger("Testing " i " [" get_char(i, 0) "]")
    c = get_char(i, 0)
    if (c == "*") {
      push_numbers(i)
      if (ratios_count == 2) {
        print "Account ratio " ratios[0] " * " ratios[1]
        acc += (ratios[0] * ratios[1])
      } else {
        print "Discard ratios count " ratios_count
      }
    }
  }
  logger("----")
}
END {
  print "Answer: " acc
}

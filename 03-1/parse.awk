BEGIN {
  FS = ""
}
function get_char(pos, line_num) {
 return substr(line[line_num], pos, 1)
}
function is_symbol(s) {
  logger("Is symbol [" s "] " (!((s == ".") || (s ~ /[0-9]/))))
  return !((s == ".") || (s ~ /[0-9]/))
}
function has_symbol(pos) {
  return is_symbol(get_char(pos - 1, -1)) || is_symbol(get_char(pos + 0, -1)) || is_symbol(get_char(pos + 1, -1)) || is_symbol(get_char(pos - 1,  0)) || is_symbol(get_char(pos + 1, 0)) || is_symbol(get_char(pos - 1,  1)) || is_symbol(get_char(pos + 0,  1)) || is_symbol(get_char(pos + 1,  1))
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

  group = ""
  group_with_symbol = 0

  for (i = 2; i <= (NF - 1); i++) {
    logger("Testing " i " [" get_char(i, 0) "]")
    c = get_char(i, 0)
    if (c ~ /[0-9]/) {
      group = group c
      if (!group_with_symbol) {
        group_with_symbol = has_symbol(i)
      }
    } else {
      if (group_with_symbol) {
        groups[groups_count++] = group
        print "Group: " group
        acc += group
      }
      group = ""
      group_with_symbol = 0
    }
  }
  logger("----")
}
END {
  print "Answer: " acc
}

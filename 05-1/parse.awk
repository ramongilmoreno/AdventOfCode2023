function logger (msg) {
  # print msg
}
function print_arr (msg, arr) {
  logger("Array " msg)
  for (i in arr) {
    logger("[" i "] is [" arr[i] "]")
  }
}

BEGIN {
  FS = "[: -]+"
}

($1 == "seeds") {
  for (i = 2; i <= NF; i++) {
    seeds[seeds_count++] = $i
  }
  next
}
function map_name (from, to) { return from "-to-" to; }
($4 == "map") {
  from = $1
  to = $3
  map[from] = to
  map_count[map_name(from, to)] = 0
  next
}
($1) {
  name = map_name(from, to)
  logger("Item - " map_count[name] " - " $0)
  range_target[name " " map_count[name]] = $1
  range_source[name " " map_count[name]] = $2
  range_length[name " " map_count[name]] = $3
  map_count[name]++
}
function min_value (a, b) {
  if (a == -1) return b
  if (b == -1) return a
  return (a <= b ? a : b)
}
function step (type, target, number) {
  logger(">>> Step type [" type "] target [" target "] number [" number "] <<<")
  if (!target) {
    logger("Return")
    return number
  }
  for (i = 0; i < map_count[map_name(type, target)]; i++) {
    aux = map_name(type, target) " " i
    if ((number >= range_source[aux]) && (number <= (range_source[aux] + range_length[aux]))) {
      logger("At range [" aux "] source [" range_source[aux] "] target [" range_target[aux] "] length [" range_length[aux] "]")
      return step(target, map[target], number - range_source[aux] + range_target[aux])
    }
  }
  return step(target, map[target], number)
}
END {
  print_arr("Seeds", seeds)
  print_arr("Map", map)
  print_arr("Count", map_count)
  print_arr("Range source", range_source)
  print_arr("Range target", range_target)
  print_arr("Range length", range_length)
  acc = -1
  for (j = 0; j < seeds_count; j++) {
    acc = min_value(acc, step("seed", map["seed"], seeds[j]))
    logger("Solved " acc)
  }
  print "Answer: " acc
}

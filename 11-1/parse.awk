BEGIN {
  FS = ""
  print "Begin"
}
{
  galaxies_rows++
  galaxies_row[galaxies_rows] = 2
  galaxies_columns = NF
  for (i = 1; i <= NF; i++) {
    if (!galaxies_column[i]) {
      galaxies_column[i] = 2
    }
    if ($i == "\#") {
      galaxies_count++
      galaxies_x[galaxies_count] = i
      galaxies_y[galaxies_count] = NR
      galaxies_row[NR] = 1
      galaxies_column[i] = 1
    }
  }
  print
}
function abs (a) { return a < 0 ? -a : a }
END {
  for (i = 1; i <= galaxies_count; i++) {
    galaxies_x_expanded[i] = 0 
    for (j = 1; j <= galaxies_x[i]; j++) {
      galaxies_x_expanded[i] += galaxies_column[j]
    }
    galaxies_y_expanded[i] = 0 
    for (j = 1; j <= galaxies_y[i]; j++) {
      galaxies_y_expanded[i] += galaxies_row[j]
    }
    print "Galaxy #" i " (" galaxies_x[i] ", " galaxies_y[i] ") -> (" galaxies_x_expanded[i] ", " galaxies_y_expanded[i] ")"
  }
  for (i = 1; i <= galaxies_columns; i++) {
    print "Column #" i " is " galaxies_column[i]
  }
  for (i = 1; i <= galaxies_rows; i++) {
    print "Row #" i " is " galaxies_row[i]
  }
  acc = 0
  for (i = 1; i <= galaxies_count; i++) {
    for (j = i; j <= galaxies_count; j++) {
      acc += abs(galaxies_x_expanded[j] - galaxies_x_expanded[i]) + abs(galaxies_y_expanded[j] - galaxies_y_expanded[i])
    }
  }
  print "Answer: " acc
}

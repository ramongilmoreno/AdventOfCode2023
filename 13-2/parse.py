import sys

def log (x):
  # print(x)
  sys.stdout.flush()
  pass

print("Begin")

class MirrorAsRows:

  def __init__(self, rows, name):
    self.name = name
    self.height = len(rows)
    self.rows = rows

  def simmetry_at (self, y, ignore):
    if ignore >= 0 and ignore == y:
      log(f"  Ignoring simmetry at {y}")
      return False
    log(f"  Checking simmetry of {y}")
    count = min(y + 1, self.height - y - 1)
    for i in range(count):
      log(f"       Mirror {self.name}")
      log(f"       at row {y}, offset {i}, count {count}")
      log(f"    Comparing {self.rows[y - i]}")
      log(f"          and {self.rows[y + 1 + i]}")
      if self.rows[y - i] != self.rows[y + 1 + i]:
        log(f"    Fails")
        return False
    log(f"    Simmetry found")
    return True

  def change (self, x, y):
    new_rows = self.rows.copy()
    new_rows[y] = f"{self.rows[y][:x]}{'#' if self.rows[y][x] == '.' else '.'}{self.rows[y][x + 1:]}"
    return MirrorAsRows(new_rows, f"{self.name} changed at ({x}, {y})")

mirrors = []

def mirrors_from_rows (rows):
  global mirrors
  width = len(rows[0])
  columns = [None] * width
  for x in range(width):
    columns[x] = "".join([y[x] for y in rows])
  mirrors.append((MirrorAsRows(rows, f"Mirror rows {len(mirrors)}"), MirrorAsRows(columns, f"Mirror column {len(mirrors)}")))

rows = None
for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}]")
  if len(line) == 0:
    if rows:
      mirrors_from_rows(rows)
      rows = None
  else:
    if rows == None:
      rows = []
    rows.append(line)

# Last mirror
if rows:
  mirrors_from_rows(rows)

acc = (0, 0)
for i in mirrors:
   height = i[0].height
   width = i[1].height
   log(f"Mirror size ({width}, {height})")
   def f (m, ignore):
     return next(((x + 1) for x in range(0, m.height - 1) if m.simmetry_at(x, ignore)), 0)
   r = (f(i[0], -1), f(i[1], -1))
   print(f" Simmetry original at {r} for mirror ({i[0].name}, {i[1].name})")
   r2 = None
   for x in range(width):
     if r2 != None:
       break
     for y in range(height):
       i_0 = i[0].change(x, y) 
       i_1 = i[1].change(y, x)
       r2 = (f(i_0, r[0] - 1), f(i_1, r[1] - 1))
       if r2[0] != 0 or r2[1] != 0:
         print(f" Found smudge at ({x}, {y}), simmetry at {r2}")
         break
       else:
         r2 = None
   r = r2
   print(f" Simmetry new at {r} for mirror ({i[0].name}, {i[1].name})")
   acc = (acc[0] + r[0], acc[1] + r[1])
   print("")
   
print(f'Answer: {acc[0] * 100 + acc[1]}')


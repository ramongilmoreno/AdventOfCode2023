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
  def simmetry_at (self, y):
    log(f"Checking simmetry of {y}")
    count = min(y + 1, self.height - y - 1)
    for i in range(count):
      log(f"       Mirror {self.name}")
      log(f"       at row {y}, offset {i}, count {count}")
      log(f"    Comparing {self.rows[y - i]}")
      log(f"          and {self.rows[y + 1 + i]}")
      if self.rows[y - i] != self.rows[y + 1 + i]:
        log(f"    Fails")
        return False
    return True

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
   log("Mirror")
   for j in i:
     log(" Rows/Cols")
     for k in range(len(j.rows)):
       log(f"  {k} {j.rows[k]}")
   def f (m): return next(((x + 1) for x in range(0, m.height - 1) if m.simmetry_at(x)), 0)
   r = (f(i[0]), f(i[1]))
   print(f"Simmetry at {r}")
   acc = (acc[0] + r[0], acc[1] + r[1])
   
print(f'Answer: {acc[0] * 100 + acc[1]}')


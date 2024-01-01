import sys

def log (x):
  print(x)
  sys.stdout.flush()
  pass

print("Begin")

rows = None
for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}]")
  if len(line) == 0:
    if rows:
      problem_from_rows(rows)
      rows = None
  else:
    if rows == None:
      rows = []
    rows.append(line)

height = len(rows)
width = len(rows[0])
# Circles will be sorted already
circles = []
empty_rows = []
acc = None 
for i in range(height):
  acc = []
  for j in range(width):
    if rows[i][j] == 'O':
      circles.append((j, i))
      acc.append('.')
    else:
      acc.append(rows[i][j])
  empty_rows.append("".join(acc))

def get (x, y): return empty_rows[y][x]

for i in empty_rows:
  log(f"{i}")
log("---")
# Rock north
acc = 0
rocked = {}
for circle in circles:
  provisional = circle
  for j in range(circle[1] - 1, -1, -1):
    candidate = (circle[0], j)
    if not(candidate in rocked) and get(candidate[0], candidate[1]) == '.':
      provisional = candidate
    else:
      break
  rocked[provisional] = circle

for i in range(height):
  for j in range(width):
    c = (j, i)
    if c in rocked:
      print('O', end="")
    else:
      print(get(j, i), end="")
  print("")

# Compute
acc = 0
for c in list(rocked.keys()):
  acc += (height - c[1])

print(f'Answer: {acc}')


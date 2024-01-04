import sys
from enum import Enum

def log (x, end = "\n"):
  # print(x, end = end)
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

class Direction:
  def __init__(self, name, index, direction, stop = -1):
    self.name = name
    self.index = index
    self.direction = direction 
    self.stop = stop
  def contrary (self, name, stop): return Direction(name, self.index, -self.direction, stop)
  def key (self, circle): return -1 * self.direction * circle[self.index]
NORTH = Direction('N', 1, -1)
WEST = Direction('W', 0, -1)
SOUTH = NORTH.contrary('S', height)
EAST = WEST.contrary('E', width)
Directions = [ NORTH, WEST, SOUTH, EAST ]

def print_circles (circles, prefix = ""):
  # return
  for i in range(height):
    log(prefix, end="")
    for j in range(width):
      c = (j, i)
      if c in circles:
        log('O', end="")
      else:
        log(get(j, i), end="")
    log("")
  log("")

acc = 0
rocked = {}
memo = {}
lasts = {}
def memo_key (circles, direction):
  return str(f"{direction.name} => {circles}")

end = 1000000000
for i in range(end):
  for j in range(len(Directions)):
    direction = Directions[j]

    log(f"Circles before {direction.name} rocking: {circles}")
    key = memo_key(circles, direction)
    if key in memo:
      log(f"* Found key in memo! {key}")
      circles = memo[key]
      continue

    # Rock in direction
    rocked = {}
    for circle in circles:
      provisional = circle
      for k in range(circle[direction.index] + direction.direction, direction.stop, direction.direction):
        candidate = list(circle)
        candidate[direction.index] = k
        candidate = tuple(candidate)
        if not(candidate in rocked) and get(candidate[0], candidate[1]) == '.':
          provisional = candidate
        else:
          break
      rocked[provisional] = provisional

    # Sort for next direction
    next_direction = Directions[(j + 1) % len(Directions)]
    circles = list(rocked.keys())
    circles.sort(key = lambda x: next_direction.key(x))
    log(f"    Circles sorted for {next_direction.name}: {circles}")
    # print_circles(circles, prefix = "  ")
    
    # Memoize it
    memo[key] = circles.copy()

  # Compute
  acc = 0
  print_circles(circles)
  for c in circles:
    acc += (height - c[1])
  print(f"Iteration {i} result {acc}")

  # Save lasts, try to find some kind of repetition
  last = str(acc)
  if last in lasts:
    lasts[last].append(i)
  else:
    lasts[last] = [ i ]

  last = lasts[last]
  steps = 2
  l = len(last)
  if l > 5:
    interval = last[l - 1] - last[l - (1 + steps)]
    if interval > 0 and (interval == last[l - (1 + steps)] - last[l - (1 + steps + steps)]):
      if (end - i - 1) % interval == 0:
        print(f"Repetition of {acc} goes to interval {interval} at repetition {i}")
        break

print(f'Answer: {acc}')


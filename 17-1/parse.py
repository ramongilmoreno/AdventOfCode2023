import sys

def log (x, end = "\n"):
  # print(x, end = end)
  sys.stdout.flush()
  pass

print("Begin")

rows = []
for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}]")
  if len(line) > 0:
    rows.append(line)

height = len(rows)
width = len(rows[0])

rows = [[int(x) for x in row] for row in rows]

def get (x, y): return rows[y][x]

class Direction:
  def __init__(self, deltaX, deltaY):
    self.deltaX = deltaX
    self.deltaY = deltaY
  def left (self): return Direction(self.deltaY, -self.deltaX)
  def right (self): return Direction(-self.deltaY, self.deltaX)

  def __repr__(self): return str((self.deltaX, self.deltaY))

NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)
WEST = Direction(-1, 0)
EAST = Direction(1, 0)
directions = [ NORTH, SOUTH, WEST, EAST ]

# Beam entry is (x, y, direction, steps in this direction, count)
# Top left cell does not add to sum: cannot start at 0 but at -get(0, 0)
beams = [ (0, 0, EAST, 0, -get(0, 0)), (0, 0, SOUTH, 0, -get(0, 0)) ]

def key_of (x):
  return str(x)

visited = {}

def get_value (x, y, direction, count):
  k = key_of((x, y))
  if k in visited:
    v = visited[k]
    k2 = key_of((direction, count))
    if k2 in v:
      return v[k2]
  else:
    return None

def set_value (x, y, direction, count, value):
  k = key_of((x, y))
  k2 = key_of((direction, count))
  if k in visited:
    v = visited[k]
    v[k2] = value
  else:
    visited[k] = {}
    visited[k][k2] = value

flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]

def print_field (): 
  for i in range(height):
    for j in range(width):
      c = "."
      k = key_of((j, i))
      if k in visited:
        c = len(visited[k].keys())
        c = "0123456789abc"[c]
      log(c, end="")
    log("")

def move (beam):
  x = beam[0]
  y = beam[1]

  if x < 0 or x >= width or y < 0 or y >= height:
    return []

  d = beam[2]
  c = beam[3]
  new_value = beam[4] + get(x, y)
  old_value = get_value(x, y, d, c) 
  if old_value == None or new_value < old_value:
    # Unvisited in this direction or smaller value
    set_value(x, y, d, c, new_value)

    # Move in every possible direction
    def apply (direction, count):
      return (x + direction.deltaX, y + direction.deltaY, direction, count, new_value)
    r = [ apply(d.left(), 0), apply(d.right(), 0) ]
    if c < 2:
      r.append(apply(d, c + 1))
    return r
  else:
    return []
  

while len(beams) > 0:
  beams = flat_map(move, beams)
  log(f"Beams after {beams}")
  print_field()

last_cell = visited[key_of((width - 1, height - 1))]
log(f"Last cell {last_cell}")
acc = min(last_cell.values())
print(f'Answer: {acc}')


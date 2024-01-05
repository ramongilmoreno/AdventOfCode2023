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

def get (x, y): return rows[y][x]

def print_field (visited): 
  for i in range(height):
    for j in range(width):
      if str((j, i)) in visited:
        log('#', end="")
      else:
        log(get(j, i), end="")
    log("")

class Direction:
  def __init__(self, deltaX, deltaY):
    self.deltaX = deltaX
    self.deltaY = deltaY
  # def perpendicular (self): return [Direction(-self.deltaY, self.deltaX), Direction(self.deltaY, -self.deltaX)]
  def left (self): return Direction(self.deltaY, -self.deltaX)
  def right (self): return Direction(-self.deltaY, self.deltaX)
  def perpendicular (self): return [self.left(), self.right()]
  def respond2 (self, x):
    if x == '.':
      return [self]
    if x == '|':
      return [self] if self.deltaY != 0 else self.perpendicular()
    elif x == '-':
      return [self] if self.deltaX != 0 else self.perpendicular()
    elif x == '/':
      if self.deltaX != 0:
        return [self.left()]
      else:
        return [self.right()]
    elif x == '\\':
      if self.deltaX != 0:
        return [self.right()]
      else:
        return [self.left()]
  def respond (self, x):
    r = self.respond2(x)
    log(f"For direction {self}, item {x}, respond with {r}")
    return r

  def __repr__(self): return str((self.deltaX, self.deltaY))

NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)
WEST = Direction(-1, 0)
EAST = Direction(1, 0)
directions = [ NORTH, SOUTH, WEST, EAST ]

for direction in directions:
  log(f"Direction {direction} perpendicular {direction.perpendicular()} left {direction.left()} right {direction.right()}")

visited_and_direction_cache = {}
def testit (beam):
  beams = [ beam ]
  visited = {}
  visited_and_direction = {}
  global visited_and_direction_cache
  flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]

  def move (beam):
    x = beam[0]
    y = beam[1]
    d = beam[2]

    if str((x, y, d)) in visited_and_direction:
      return []

    if x < 0 or x >= width or y < 0 or y >= height:
      return []

    visited[str((x, y))] = (x, y)
    vad_key = str((x, y, d))
    visited_and_direction[vad_key] = True

    if vad_key in visited_and_direction_cache:
      return visited_and_direction_cache[vad_key]

    item = get(x, y)
    r = list(map(lambda i: (x + i.deltaX, y + i.deltaY, i), d.respond(item)))
    visited_and_direction_cache[vad_key] = r
    return r

  while len(beams) > 0:
    beams = flat_map(move, beams)
    log(f"Beams after {beams}")
    print_field(visited)
    
  r = len(visited.keys())
  print(f"For beam {beam} energized is {r}")
  return r

acc = -1
for x in range(width):
  acc = max(acc, testit((x, 0, SOUTH)), testit((x, height - 1, NORTH)))
for y in range(height):
  acc = max(acc, testit((0, y, EAST)), testit((width - 1, y, WEST)))

print(f'Answer: {acc}')


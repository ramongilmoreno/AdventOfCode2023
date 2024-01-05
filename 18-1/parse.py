import sys

def log (x, end = "\n"):
  # print(x, end = end)
  sys.stdout.flush()
  pass

print("Begin")

class Direction:
  def __init__(self, deltaX, deltaY):
    self.deltaX = deltaX
    self.deltaY = deltaY
  def left (self): return Direction(self.deltaY, -self.deltaX)
  def right (self): return Direction(-self.deltaY, self.deltaX)

  def __repr__(self): return str((self.deltaX, self.deltaY))

UP = Direction(0, -1)
DOWN = Direction(0, 1)
LEFT = Direction(-1, 0)
RIGHT = Direction(1, 0)
directions = {
  'U': UP,
  'D': DOWN,
  'L': LEFT,
  'R': RIGHT
}

# Read input
rows = []
for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}]")
  if len(line) > 0:
    elements = line.split(" ")
    rows.append((directions[elements[0]], int(elements[1])))

# Compute field
x_max = 0
x_min = 0
y_max = 0
y_min = 0
current = (0, 0)
for r in rows:
  log(f"Movement {r}")
  direction = r[0]
  quantity = r[1]
  current = (current[0] + (direction.deltaX * quantity), current[1] + (direction.deltaY * quantity))
  x_max = max(x_max, current[0])
  x_min = min(x_min, current[0])
  y_max = max(y_max, current[1])
  y_min = min(y_min, current[1])

width = (x_max - x_min) + 1
height = (y_max - y_min) + 1
log(f"Width {width} height {height}")

# It't a trap!
# https://stackoverflow.com/a/44382900
# field = [ [ '.' ] * width ] * height

field = [ [ '.' ] * width for i in range(height) ]
def get (x, y): return field[y][x]

def print_field ():
  for y in range(height):
    for x in range(width):
      log(get(x, y), end="")
    log("")


def connector (direction1, direction2):
  start = 'X'
  if direction2 == direction1:
    start = '#'
  elif direction1 == UP and direction2 == RIGHT:
    start = '/'
  elif direction1 == DOWN and direction2 == LEFT:
    start = '/'
  elif direction1 == UP and direction2 == LEFT:
    start = '\\'
  elif direction1 == DOWN and direction2 == RIGHT:
    start = '\\'
  elif direction1 == RIGHT and direction2 == UP:
    start = '/'
  elif direction1 == LEFT and direction2 == DOWN:
    start = '/'
  elif direction1 == RIGHT and direction2 == DOWN:
    start = '\\'
  elif direction1 == LEFT and direction2 == UP:
    start = '\\'
  return start

# Layout edge
current = (0 - x_min, 0 - y_min)
field[current[1]][current[0]] = '#'
for i in range(len(rows)):
  r = rows[i]
  direction = r[0]
  last_direction = rows[(i - 1) % len(rows)][0]
  next_direction = rows[(i + 1) % len(rows)][0]
  quantity = r[1]
  log(f"Moving {direction} for {quantity} from {current}")
  field[current[1]][current[0]] = connector(last_direction, direction)
  for j in range(quantity):
    current = (current[0] + direction.deltaX, current[1] + direction.deltaY)
    # log(f"Setting {current} index {j}")
    field[current[1]][current[0]] = '#'
  field[current[1]][current[0]] = connector(direction, next_direction)

# Fill inner
acc = 0
for y in range(height):
  count = 0
  last_connector = None
  for x in range(width):
    c = get(x, y)
    acc += 1
    if c == '/' or c == '\\':
      if last_connector == None:
        last_connector = c
      else:
        if last_connector == c:
          # Account crossings /--/ or \--\
          count += 1
        last_connector = None
    elif c == '#':
      if last_connector == None:
        # Vertical edge
        count += 1
    elif c == '.':
      if count % 2 == 1:
        # Inbounds
        field[y][x] = 'X'
      else:
        # Discount
        acc -= 1
    else:
      raise SystemExit(f'Unknown character {c}')

print_field()

flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]

print(f'Answer: {acc}')


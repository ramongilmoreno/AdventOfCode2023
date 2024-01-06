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
directions_indexed = [ RIGHT, DOWN, LEFT, UP ]

# Read input
rows = []
for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}]")
  if len(line) > 0:
    elements = line.split(" ")
    rows.append((directions[elements[0]], int(elements[1])))
    continue
    # hex_value = int(f"0x{elements[2][2:-1]}", 0)
    # log(f"Hex value {hex_value}, direction {hex_value % 16} length {hex_value // 16}")
    # rows.append((directions_indexed[hex_value % 16], hex_value // 16))

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
print(f"Width {width}, height {height}")

# It't a trap!
# https://stackoverflow.com/a/44382900
# field = [ [ '.' ] * width ] * height

field = [ [ ('.', 0, width ) ] for i in range (height) ]

flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]
def insert (y, entries):
  min_x = min(map(lambda x: x[1], entries))
  width = sum(map(lambda x: x[2], entries))
  def f (item):
    if min_x >= item[1] and min_x < (item[1] + item[2]):
      # ('.', 4, 10)
      # insert              ('/', 6, 1), ('#', 7, 3), ('/', 10, 1)
      #                     min_x = 6, width = 5
      # result ('.', 4, 2), ('/', 6, 1), ('#', 7, 3), ('/', 10, 1), ('.', 11, 3)
      return filter(lambda x: x[2] > 0, [ (item[0], item[1], min_x - item[1]), *entries, (item[0], min_x + width, item[1] + item[2] - min_x - width) ])
    else:
      return [ item ]
  field[y] = list(flat_map(f, field[y]))

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
for i in range(len(rows)):
  r = rows[i]
  direction = r[0]
  last_direction = rows[(i - 1) % len(rows)][0]
  next_direction = rows[(i + 1) % len(rows)][0]
  quantity = r[1]
  log(f"Moving {direction} for {quantity} from {current}")
  # field[current[1]][current[0]] = connector(last_direction, direction)
  if direction.deltaX == 1:
    # Horizontal insert
    # insert(current[1], [(connector(last_direction, direction), current[0], 1), ('#', current[0] + 1, quantity - 2), (connector(direction, next_direction), current[0] + quantity - 2, 1)])
    insert(current[1], [(connector(last_direction, direction), current[0], 1), ('#', current[0] + 1, quantity - 1)])
    current = (current[0] + quantity, current[1])
  if direction.deltaX == -1:
    # Horizontal insert in reverse
    # insert(current[1], [(connector(direction, next_direction), current[0] - quantity, 1), ('#', current[0] - quantity + 1, quantity - 2), (connector(last_direction, direction), current[0], 1)])
    insert(current[1], [('#', current[0] - quantity, quantity), (connector(last_direction, direction), current[0], 1)])
    current = (current[0] - quantity, current[1])
  if direction.deltaY != 0:
    for j in range(quantity):
      if j == 0:
        insert(current[1], [(connector(last_direction, direction), current[0], 1)])
      # elif j == (quantity - 1):
        # insert(current[1], [(connector(direction, next_direction), current[0], 1)])
      else:
        insert(current[1], [('#', current[0], 1)])
      current = (current[0] + direction.deltaX, current[1] + direction.deltaY)

def print_field ():
  for row in field:
    for item in row:
      log("".join([ item[0] ] * item[2]), end="")
    log("")

print_field()

# Fill inner
acc = 0
for row in field:
  count = 0
  last_connector = None
  for item in row:
    c = item[0]
    width = item[2]
    acc += width 
    if c == '/' or c == '\\':
      if last_connector == None:
        last_connector = c
      else:
        if last_connector == c:
          # Account crossings /--/ or \--\
          count += width
        last_connector = None
    elif c == '#':
      if last_connector == None:
        # Vertical edge
        count += width
    elif c == '.':
      if count % 2 == 1:
        # Inbounds
        pass
      else:
        # Discount
        acc -= width
    else:
      raise SystemExit(f'Unknown character {c}')

print(f'Answer: {acc}')


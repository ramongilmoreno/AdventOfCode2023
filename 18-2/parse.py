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
    #
    # This commented section allow testing the calculation in part 1
    #
    # rows.append((directions[elements[0]], int(elements[1])))
    # continue
    hex_value = int(f"0x{elements[2][2:-1]}", 0)
    log(f"Hex value {hex_value}, direction {hex_value % 16} length {hex_value // 16}")
    rows.append((directions_indexed[hex_value % 16], hex_value // 16))

# Compute field
current = (0, 0)
vertices = []
perimeter = 0
for r in rows:
  log(f"Movement {r}")
  direction = r[0]
  quantity = r[1]
  current = (current[0] + (direction.deltaX * quantity), current[1] + (direction.deltaY * quantity))
  vertices.append(current)
  perimeter += quantity

log(f"Vertices {vertices}, perimeter {perimeter}")

# Shoelace formula 
# https://en.wikipedia.org/wiki/Shoelace_formula
top = 0
bottom = 0
# vertices = [(0, 1), (1, 1), (1, 0), (0, 0)]
# vertices = [(1, 6,), (3, 1), (7, 2), (4, 4), (8, 5)] 
for i in range(len(vertices)):
  vertex_0 = vertices[i]
  vertex_1 = vertices[(i + 1) % len(vertices)]
  top += (vertex_0[0] * vertex_1[1])
  bottom += (vertex_0[1] * vertex_1[0])

# Why + 1 at the end? Assume that a closed polygon at [(0, 0), (0, 0), (0, 0),
# (0, 0)] would occupy at least 1 "#"
acc = ((top - bottom) // 2) + (perimeter // 2) + 1
print(f'Answer: {acc}')



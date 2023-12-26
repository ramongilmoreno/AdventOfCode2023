import sys
import math

def log (x):
  # print(x)
  pass

# | is a vertical pipe connecting north and south. 
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
north = (0, -1)
east = (1, 0)
def reverse (x): return (-x[0], -x[1])
south = reverse(north)
west = reverse(east)
directions = {
  "|": { north: south },
  "-": { east: west },
  "L": { north: east },
  "J": { north: west },
  "7": { south: west },
  "F": { south: east }
}
for c in directions.items():
  log(f"Direction BEFORE {str(c)}")
  c1 = c[1]
  v = list(c[1].items())[0]
  v_key = v[0]
  v_value = v[1]
  del c1[v_key]
  c1[reverse(v_value)] = v_key
  c1[reverse(v_key)] = v_value
  log(f"Direction  AFTER {str(c)}")
log(f'Directions {str(directions)}')

print("Begin")

maze = []
start = None
for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}] position {len(maze)}")
  s = line.find('S')
  if s != -1:
    start = (s, len(maze))
  if len(line) > 0:
    maze.append(line)
log(f'Maze {str(maze)}, start at {start}')

path = []
current = start
def cell (pos): return maze[pos[1]][pos[0]]
def travel (start_position, direction):
  acc = []
  while True:
    target_position = (start_position[0] + direction[0], start_position[1] + direction[1])
    target_cell = cell(target_position)
    if target_cell == 'S':
      return acc
    if target_cell == '.':
      return None
    next_direction = directions[target_cell].get(direction)
    if next_direction == None:
      # No way through the given direction
      return None
    else:
      start_position = target_position
      direction = next_direction
      acc = acc + list(target_cell)
      # Cannot be made recursive given the size of the problem
      # return travel(target_position, next_direction, acc + list(target_cell))

paths = list(map(lambda x: travel(start, x), [ north, south, east, west ]))
log(f'Paths: {str(paths)}')
paths = list(map(lambda x: len(x) if x != None else 0, paths))
log(f'Paths: {str(paths)}')
answer = math.ceil(max(*paths) / 2)

print(f'Answer: {str(answer)}')


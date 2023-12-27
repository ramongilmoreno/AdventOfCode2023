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

current = start
def cell (pos): return maze[pos[1]][pos[0]]
path = None
def travel (start_position, direction):
  absolute_start_direction = direction
  global path
  acc = []
  while True:
    target_position = (start_position[0] + direction[0], start_position[1] + direction[1])
    target_cell = cell(target_position)
    if target_cell == 'S':
      # Find which symbol closes the circuit
      found = next(x[0] for x in directions.items() if x[1].get(reverse(absolute_start_direction)) != None and x[1].get(direction) != None)
      acc.insert(0, (found, start))
      path = acc
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
      acc.append((target_cell, target_position))
      # Cannot be made recursive given the size of the problem
      # return travel(target_position, next_direction, acc + list(target_cell))

for i in [ north, south, east, west ]:
  travel(start, i)
log(f'Path: {str(path)}')
maze_path = {}
for i in path:
  maze_path[i[1]] = i[0]
log(f'Maze path: {maze_path}')

answer = 0
for y in range(len(maze)):
  count = 0
  last_in = None
  for x in range(len(maze[y])):
    p = (x, y)
    c = maze_path.get(p)
    if c != None:
      if c == '|':
        count += 1
      elif c == 'F' or c == 'L':
        last_in = c
      # Only account on F--J
      elif c == 'J' and last_in == 'F':
        count += 1
      # Only account on L--7
      elif c == '7' and last_in == 'L':
        count += 1
      count = count % 2
    else:
      if count == 0:
        c = 'O'
      else:
        c = 'I'
        answer += 1
    print(c, end = '')
  print()

print(f'Answer: {str(answer)}')


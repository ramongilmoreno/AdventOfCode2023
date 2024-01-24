import sys
import functools 
from ast import literal_eval

def log (x, end = "\n"):
  # print(x, end = end)
  sys.stdout.flush()
  pass

print("Begin")

current = {}
rows = []

def key (coords): return str(coords)
for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}]")
  if len(line) > 0:
    rows.append(line)
    try:
      index = line.index('S')
      current[key((0, 0))]= { (index, len(rows) - 1) }
    except ValueError:
      pass

height = len(rows)
width = len(rows[0])

def get (x, y):
  x = x % width
  y = y % height
  return rows[y][x]

def in_cluster (cluster, coords, origin):
  k = key(((coords[0] + origin[0] * width) // width, (coords[1] + origin[1] * height) // height))
  if k in cluster:
    coords = (coords[0] % width, coords[1] % height)
    return coords in cluster[k]
  else:
    return False
  
def add_to_cluster (cluster, coords, origin):
  k = key(((coords[0] + origin[0] * width) // width, (coords[1] + origin[1] * height) // height))
  coords = (coords[0] % width, coords[1] % height)
  if k in cluster:
    cluster[k].add(coords)
  else:
    cluster[k] = { coords }

def print_field (visited): 
  field_cells = sorted(map(literal_eval, visited.keys()))
  log(f'Field cells {field_cells}')
  min_x = min(map(lambda x: x[0], field_cells))
  max_x = max(map(lambda x: x[0], field_cells))
  min_y = min(map(lambda x: x[1], field_cells))
  max_y = max(map(lambda x: x[1], field_cells))
  for i in range(min_y, max_y + 1):
    for j in range(height):
      for k in range(min_x, max_x + 1):
        for l in range(width):
          if in_cluster(visited, (l, j), (k, i)):
            log('O', end="")
          else:
            log(get(l, j), end="")
      log("")

memo = {}
def once (acc, item):
  # log(f'Once for acc {acc}, item {item}')
  # Try north, south, east and west
  try_these = [(item[0], item[1] - 1), (item[0], item[1] + 1), (item[0] + 1, item[1]), (item[0] - 1, item[1])] 
  for i in try_these:
    if get(i[0], i[1]) != '#':
      acc.add(i)
  return acc

# for i in range(26501365):
for i in range(500):
  if i % 100 == 0:
    print(f'Run {i}')
    sys.stdout.flush()
  new_current = {}
  for j in current.items():
    origin = literal_eval(j[0])
    values = key(sorted(list(j[1])))
    result = None
    if values in memo:
      result = memo[values]
    else:
      result = functools.reduce(once, j[1], set())
      memo[values] = result
    for k in result:
      add_to_cluster(new_current, k, origin)

  current = new_current
  # log(f'After {current}')
  # print_field(current)

print(f'Answer: {functools.reduce(lambda acc, x: acc + len(x), current.values(), 0)}')


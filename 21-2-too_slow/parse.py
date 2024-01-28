import sys
import functools 
from ast import literal_eval

def log (x, end = "\n"):
  print(x, end = end)
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

def once (acc, item):
  # log(f'Once for acc {acc}, item {item}')
  # Try north, south, east and west
  try_these = [(item[0], item[1] - 1), (item[0], item[1] + 1), (item[0] + 1, item[1]), (item[0] - 1, item[1])] 
  for i in try_these:
    if get(i[0], i[1]) != '#':
      acc.add(i)
  return acc

memo = {}
memo_it = {}
memo_history = {}
memo_history_values = {}
alternating = {}

def add_to_memo_history (block_coords, index, values):
  k = key(block_coords)
  if not k in memo_history:
    memo_history[k] = []
    memo_history_values[k] = []
  memo_history[k].append(index)
  memo_history_values[k].append(values)

# for i in range(26501365):
for i in range(500):
  if i % 100 == 0:
    print(f'Run {i}')
    sys.stdout.flush()
  new_current = {}
  for j in current.items():
    origin = literal_eval(j[0])

    # Locate alternating
    repetition = False
    if j[0] in alternating:
      # print(f"Alternating {alternating[j[0]]}")
      new_current[j[0]] = alternating[j[0]][i % 2]
      repetition = True
    # Detect repetitions
    elif j[0] in memo_history:
      history = memo_history[j[0]]
      l = len(history)
      if l >= 3:
        if history[l - 0 - 1] == history[l - 2 - 1]:
          history_values = memo_history_values[j[0]]
          if i % 2 == 0:
            alternating[j[0]] = [ history_values[l - 1 - 1], history_values[l - 0 - 1] ]
          else:
            alternating[j[0]] = [ history_values[l - 0 - 1], history_values[l - 1 - 1] ]
          new_current[j[0]] = alternating[j[0]][i % 2]
          memo_history[j[0]] = None
          repetition = True
    if not repetition: 
      values = key(sorted(list(j[1])))
      result = None
      iteration_number = i
      if values in memo:
        result = memo[values]
        iteration_number = memo_it[values]
      else:
        result = functools.reduce(once, j[1], set())
        memo[values] = result
        memo_it[values] = i
      filtered = set(filter(lambda x: x[0] >= 0 and x[0] < width and x[1] >= 0 and x[1] < height, result))
      add_to_memo_history(origin, iteration_number, filtered)
      for k in result:
        add_to_cluster(new_current, k, origin)

  current = new_current
  # log(f'After {current}')
  # print_field(current)
  # log(f'Sorted history {memo_history}')
  # print(f'Iteration {i} : {functools.reduce(lambda acc, x: acc + len(x), current.values(), 0)}')

print(f'Answer: {functools.reduce(lambda acc, x: acc + len(x), current.values(), 0)}')


import sys
import functools 

def log (x, end = "\n"):
  # print(x, end = end)
  sys.stdout.flush()
  pass

print("Begin")

current = set()
rows = []
for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}]")
  if len(line) > 0:
    rows.append(line)
    try:
      index = line.index('S')
      current.add((index, len(rows) - 1)) 
    except ValueError:
      pass

height = len(rows)
width = len(rows[0])

def get (x, y):
  # Render out of bounds
  if x < 0 or x >= width or y < 0 or y >= height:
    return '#'
  else:
    return rows[y][x]

def print_field (visited): 
  for i in range(height):
    for j in range(width):
      if (j, i) in visited:
        log('O', end="")
      else:
        log(get(j, i), end="")
    log("")

def once (acc, item):
  # log(f'Once for acc {acc}, item {item}')
  # Try north, south, east and west
  try_these = [(item[0], item[1] - 1), (item[0], item[1] + 1), (item[0] + 1, item[1]), (item[0] - 1, item[1])] 
  for i in try_these:
    if get(i[0], i[1]) != '#':
      acc.add(i)
  return acc

for i in range(64):
  log(f'Run {i}')
  current = functools.reduce(once, current, set())
  log(f'After {current}')
  print_field(current)


print(f'Answer: {len(current)}')


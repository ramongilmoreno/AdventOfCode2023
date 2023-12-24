import sys
import re
import math

# https://dev.to/turbaszek/flat-map-in-python-3g98
def flat_map(f, xs):
  ys = []
  for x in xs:
    ys.extend(f(x))
  return ys

def log (x):
  # print(x)
  pass

print("Begin")
path = input().strip()
log(f'           Path: {path}')
path = list(map(lambda x: 0 if x == 'L' else 1, path))
log(f'  Path as index: {path}')

def clean (x):
  return re.search('([0-9A-Z]+)', x)[0]

# Define map as a dictionary
m = { }
for line in sys.stdin:
  line = line.strip()
  elements = line.split()
  log(f"[{line}] elements {str(elements)}")
  if len(elements) > 0:
    f = elements[0]
    l = clean(elements[2])
    r = clean(elements[3])
    log(f"-> from: {f}, left: {l}, right: {r}")
    m[f] = (l, r)
log(f'Map {m}')

# Seach paths
current = list(filter(lambda x: x.endswith('A'), m.keys()))
current_goals_steps = list([0 for i in current])
log(f'Start {current}')
count = 0
def direction (): return path[count % len(path)]
# while any(not(x.endswith('Z')) for x in current):
while any((x == 0) for x in current_goals_steps):
  current = list(map(lambda x: m[x][direction()], current))
  count += 1
  log(f'-> Step {current}')
  reached = [i for i in range(len(current)) if current[i].endswith('Z')]
  for i in reached:
    current_goals_steps[i] = count

print("Goals")
print(list(current_goals_steps))

print(f'Answer: {math.lcm(*current_goals_steps)}')


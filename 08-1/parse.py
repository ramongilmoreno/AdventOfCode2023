import sys
import re

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
  return re.search('([A-Z]+)', x)[0]

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
current = "AAA"
count = 0
def direction (): return path[count % len(path)]
while current != "ZZZ":
  log(f'Step {count + 1} at {current} direction {direction()} -> {m[current][direction()]}')
  current = m[current][direction()]
  count += 1

print(f'Answer: {count}')


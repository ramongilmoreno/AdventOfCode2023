import sys

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
for line in sys.stdin:
  line = line.strip()
  elements = line.split()
  log("[" + line + "] elements " + str(elements))
  if line == "":
    log("Empty line")
  elif line.startswith("seeds:"):
    elements = [int(i) for i in elements[1:]]
    seeds = list(zip(elements[0::2], elements[1::2]))
    seeds = list(map(lambda x: (x[0], x[0] + x[1] - 1), seeds))
    log("Seeds: " + str(seeds))
    targets = []
    log("Targers: " + str(targets))
  elif line.endswith("map:"):
    seeds = seeds + targets
    targets = []
    print("New map starts with seeds: " + str(seeds))
  else:
    destination, start, length = [int(i) for i in elements]
    log("Regular line 1: " + str(destination) + ", " + str(start) + ", " + str(length))
    delta = destination - start
    start = (start, start + length - 1)
    print("Regular line 2: " + str(start) + ", delta: " + str(delta))
    def intersection (i1, i2):
      if i1[0] > i2[0]:
        # Sort to assume i1 is always before i2
        return intersection(i2, i1)
      elif i1[1] < i2[0]:
        # No overlap
        return None
      else:
        # Some intersection exist
        start = max(i1[0], i2[0])
        end = min(i1[1], i2[1])
        return (start, end)
    def split_interval (i):
      log("Splitting interval " + str(i))
      r = []
      inter = intersection(i, start)
      if inter is not None:
        log("Found intersection " + str(inter))
        targets.append((inter[0] + delta, inter[1] + delta))
        # Check where intersection happens
        if i[0] < inter[0]:
          r.append((i[0], inter[0] - 1))
        if (inter[1] < i[1]):
          r.append((inter[1] + 1, i[1]))
      else:
        r.append(i)
      log("Split returned " + str(r))
      return r
 
    log("Start: " + str(seeds))
    seeds = flat_map(split_interval, seeds)
    log("End 1: " + str(seeds))
    log("End 2: " + str(targets))
print("End")
seeds = seeds + targets
print("Answer: " + str(min(list(map(lambda x: x[0], seeds)))))


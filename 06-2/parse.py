from functools import reduce
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
def clean (s):
  return int("".join(s.strip().split()[1:]))
time = clean(input())
log("Time " + str(time))
distance = clean(input())
log("Distance " + str(distance))

# Compute all cases reached distance
total = 0
def reach (t):
  global total
  if ((time - t) * t) > distance:
    total += 1
for i in range(0, time):
  reach(i)
print("Answer: " + str(total))
  

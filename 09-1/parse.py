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

problems = []
for line in sys.stdin:
  line = line.strip()
  elements = line.split()
  log(f"[{line}] elements {str(elements)}")
  if len(elements) > 0:
    problems.append([int(x) for x in elements])

log(f'Problems {str(problems)}')
def solve (p):
  if all([x == 0 for x in p]):
    return 0
  else:
    acc = p[0] 
    r = []
    for i in p[1::]:
      r.append(i - acc)
      acc = i
    return p[len(p) - 1] + solve(r)
     

answer = list(map(solve, problems))
log(f'Intermediate answer: {str(answer)}')
answer = sum(answer)
print(f'Answer: {str(answer)}')


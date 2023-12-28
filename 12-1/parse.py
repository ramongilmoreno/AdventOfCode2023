import sys

def log (x):
  # print(x)
  pass

print("Begin")

acc = 0

def solutions (problem, index):
  r = []
  acc = 0
  for i in range(index, len(problem)):
    c = problem[i]
    if c == '#' or c == '?':
      acc += 1
    elif c == '.':
      if acc > 0:
        r.append(acc)
        acc = 0
  # Include last
  if acc > 0:
    r.append(acc)
  return r

def compatible_solutions (candidate, real):
  return True
  # This didn't work, leaving for Part 2 if worth it
  for i in range(min(len(candidate), len(real))):
    if candidate[i] < real[i]:
      return False
  return True

acc = 0
def travel (problem, index, solution):
  global acc
  candidate = solutions(problem, 0)
  if compatible_solutions(candidate, solution):
    try:
      i = problem.index('?', index)
      problem_a = problem.copy()
      problem_a[i] = '#'
      travel(problem_a, i + 1, solution)
      problem_b = problem.copy()
      problem_b[i] = '.'
      travel(problem_b, i + 1, solution)
    except ValueError:
      # More ? not found, must check solutions are exactly the same
      if candidate == solution:
        acc += 1
        log(f'  Problem [{problem}] is the solution to {solution}, acc is {acc}')
  else:
    log(f' Discarded [{problem}] for solution {solution}')
  
for line in sys.stdin:
  line = line.strip()
  elements = line.split()
  log(f"[{line}] elements {str(elements)}")
  if len(elements) > 0:
    problem = list(elements[0])
    solution = [int(x) for x in elements[1].split(",")]
    log(f"Problem [{problem}] solution {solution}")
    log(f"Solutions {solutions(problem, 0)}")
    travel(problem, 0, solution)
    log(f"Valid")

print(f'Answer: {acc}')


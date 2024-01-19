import sys

def log (x):
  # print(x)
  pass

print("WARNING!!!! This implementation of 12-2 does not solve the full input.txt")
print("Begin")

def repeat (str, count): return "".join([ str ] * count)

# Compare a candidate solution to the problem wildcard string
def equivalent (wildcards, working, must_be_equals):
  l_problem = len(problem)
  l_working = len(working)
  for i in range(l_problem if must_be_equals else min(l_problem, l_working)):
    c_wildcards = wildcards[i]
    c_working = working[i]
    if c_wildcards != c_working:
      if c_working == ',':
        return c_wildcards != '#'
      else:
        if c_wildcards != '?':
          if c_wildcards != c_working:
            return False
  return True

acc = 0
def travel (problem, working):
  log(f" Testing [{working}] for [{problem}]")
  if not equivalent(problem, working, False):
    return
  global acc
  l_problem = len(problem)
  l_working = len(working)
  if l_working > l_problem:
    # Nothing else to try here
    log(f'  Not valid solution')
    return
  try:
    index = working.index(",")
    for i in range(1, l_problem - l_working + 2):
      travel(problem, working[:index] + repeat('.', i) + working[index + 1:])
  except ValueError:
    if (l_problem == l_working) and equivalent(problem, working, True):
      log(f'  Valid solution')
      acc += 1

count = 0
for line in sys.stdin:
  line = line.strip()
  elements = line.split()
  log(f"Line [{line}] elements {str(elements)}")
  if len(elements) > 0:
    count += 1
    times = 5
    problem = elements[0]
    problem = "?".join([problem for i in range(times)])
    problem = "." + problem + "."
    solution = [int(x) for x in elements[1].split(",")]
    solution = solution * times
    working = "," + ",".join([repeat('#', i) for i in solution]) + ","
    print(f"Problem #{count} - [{problem}] solution {solution}, working [{working}]")
    sys.stdout.flush() 
    travel(problem, working)

print(f'Answer: {acc}')


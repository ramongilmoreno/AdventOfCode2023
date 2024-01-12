import sys
import json 
import re

def log (x, end = "\n"):
  # print(x, end = end)
  sys.stdout.flush()
  pass

print("Begin")

def greater_than (a, b): return a > b
def smaller_than (a, b): return a < b

# Read workflows
workflows = {}
for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}]")
  if len(line) > 0:
    elements = line.split("{")
    name = elements[0]
    steps = elements[1][:-1].split(',')
    log(f"Workflows {name} {steps}")
    def parse_steps (step):
      if step.find(':') != -1:
        step = step.split(':')
        condition = step[0]
        target = step[1]
        f = None
        op = None
        if condition.find('<') != -1:
          condition = condition.split('<')
          f = smaller_than
        else:
          condition = condition.split('>')
          f = greater_than
        field = condition[0] 
        value = int(condition[1])
        condition = f
        log(f"Rule condition {field} {condition} {value}  -> {target}")
        def r (part):
          if condition(part[field], value):
            return target
          else:
            return None
        return { "function": r, "target": target, "condition_field": field, "condition_param": value, "condition_operation": f.__name__}
      else:
        log(f"Rule direct -> {step}")
        return { "function": lambda x: step, "target": step, "condition_field": None }
    workflows[name] = list(map(parse_steps, steps))
    log(f"Workflows {workflows}")
  else:
    break

log(f"Workflow {workflows}")

def steps_for_target (target):
  r = []
  for workflow_name in workflows:
    workflow = workflows[workflow_name]
    if next((condition for condition in workflow if condition["target"] == target), None) != None:
      for condition in workflow:
        r.append(condition)
      r.extend(steps_for_target(workflow_name))
  return r

smaller_set_of_steps = steps_for_target('A')
log(f"Steps for target {smaller_set_of_steps}")

# Compute candidate intervals based on workflows conditions for each field
intervals_count = 1
def intervals (key):
  global intervals_count
  greater_than = set()
  smaller_than = set()
  for condition in smaller_set_of_steps:
    if condition["condition_field"] == key:
      op = condition["condition_operation"]
      if op == "greater_than":
        greater_than.add(condition["condition_param"])
      else:
        smaller_than.add(condition["condition_param"])
  greater_than.add(4000)
  r = []
  all = list(greater_than.union(smaller_than))
  all.sort()
  current = (1, None)
  for v in all:
     if v in smaller_than and v in greater_than:
       r.append((current[0], v - 1))
       r.append((v, v))
       current = (v + 1, None)
     elif v in smaller_than:
       r.append((current[0], v - 1))
       current = (v, None)
     elif v in greater_than:
       r.append((current[0], v))
       current = (v + 1, None)
  print(f"For {key} intervals count {len(r)}")
  sys.stdout.flush()
  intervals_count *= len(r)
  return r
intervals_x = intervals('x')
intervals_m = intervals('m')
intervals_a = intervals('a')
intervals_s = intervals('s')

def size_of_interval (x):
  return x[1] - x[0] + 1
def all_options ():
  for i_x in intervals_x:
    for i_m in intervals_m:
      for i_a in intervals_a:
        for i_s in intervals_s:
          yield { "x": i_x, "m": i_m, "a": i_a, "s": i_s, "size": size_of_interval(i_x) * size_of_interval(i_m) * size_of_interval(i_a) * size_of_interval(i_s) }

acc = 0
count = 0
for o in all_options():

  # Prepare agenda with the first value of each interval
  agenda = [('in', { "x": o["x"][0], "m": o["m"][0], "a": o["a"][0], "s": o["s"][0], "size": o["size"]})]
  log(f"Agenda {agenda}")

  while len(agenda) > 0:
    log(f'Agenda {agenda}')
    # Process each item
    r = []
    for i in agenda:
      part = i[1]
      workflow = workflows[i[0]]
      skip = False
      for j in range(len(workflow)):
        log(f'Processing rule {j}') 
        if not skip:
          s = workflow[j]
          r2 = s["function"](part)
          if r2 != None:
            log(f"Applied workflow {i[0]}, rule {j} to part {part} -> {r2}")
          if r2 == 'A':
            acc += part["size"]
            skip = True
          elif r2 == 'R':
            skip = True
          elif r2 != None:
            r.append((r2, part))
            skip = True
    agenda = r
  count += 1
  if count % 100000 == 0:
    print(f"Acc at iteration {count} of {intervals_count} ({(count / intervals_count) * 100} %) is {acc}")

print(f'Answer: {acc}')


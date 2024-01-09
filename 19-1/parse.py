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
        return r
      else:
        log(f"Rule direct -> {step}")
        return lambda x: step
    workflows[name] = list(map(parse_steps, steps))
    log(f"Workflows {workflows}")
  else:
    break

# Read parts
parts = []
for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}]")
  if len(line) > 0:
    line = re.sub('([a-z]+)=', '"\\1":', line)
    line = json.loads(line)
    log(f"Part {line}")
    parts.append(line)

# Prepare agenda
agenda = list(map(lambda x: ('in', x), parts))

R = []
A = []
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
        r2 = s(part)
        if r2 != None:
          print(f"Applied workflow {i[0]}, rule {j} to part {part} -> {r2}")
        if r2 == 'A':
          A.append(part)
          skip = True
        elif r2 == 'R':
          R.append(part)
          skip = True
        elif r2 != None:
          r.append((r2, part))
          skip = True
  agenda = r


log(f'A: {A}')
log(f'R: {R}')

acc = 0
for i in A:
  for j in i.values():
    acc += j

print(f'Answer: {acc}')


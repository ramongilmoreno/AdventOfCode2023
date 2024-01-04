import sys
import re

def log (x):
  print(x)
  sys.stdout.flush()
  pass

print("Begin")

items = []
current = []
current_operation = None

def add ():
  global items, current, current_operation
  if len(current) > 0:
    values = "".join(current).split(" ")
    if len(values[1]) == 0:
      v = 0
    else:
      v = int(values[1])
    items.append((values[0], current_operation, v))
  current = []
  current_operation = None

while c := sys.stdin.read(1):
  if c == ',':
    add()
  elif c == '-' or c == '=':
    current_operation = c
    current.append(' ')
  elif ord(c) == 13 or ord(c) == 10:
    log("New line")
  else:
    current.append(c)

add()

def hash (input):
  r = 0
  for i in input:
    r += i
    r *= 17
    r %= 256
  return r

def hash_string (input):
  return hash(map(lambda x: ord(x), [*input]))
  
boxes = [[]] * 256
for i in items:
  h = hash_string(i[0])
  log(f"Item {i}, hash is {h}")
  o = i[1]
  if o == '-':
    boxes[h] = [x for x in boxes[h] if x[0] != i[0]]
  else:
    found = False
    def modify (x):
      global found
      if x[0] == i[0]:
        found = True
        return (x[0], i[2])
      return x
    boxes[h] = [modify(i) for i in boxes[h]]
    if not found:
      boxes[h].append((i[0], i[2]))

log(f"Hash of HASH is {hash_string('HASH')}")
log(f"Boxes {boxes}")
# acc = sum(map(hash, items))

acc = 0
for i in range(len(boxes)):
  box = boxes[i]
  for j in range(len(box)):
    acc += (i + 1) * (j + 1) * box[j][1]

print(f'Answer: {acc}')


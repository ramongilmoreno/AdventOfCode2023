import sys

def log (x):
  # print(x)
  sys.stdout.flush()
  pass

print("Begin")

items = []
current = []

def add ():
  global items, current
  if len(current) > 0:
    items.append(current.copy())
  current = []

while c := sys.stdin.read(1):
  o = ord(c)
  log(f"Char [{c}], ASCII {o}")
  if c == ',':
    add()
  elif o == 13 or o == 10:
    log("New line")
  else:
    current.append(o)

add()

def hash (input):
  r = 0
  for i in input:
    r += i
    r *= 17
    r %= 256
  return r

  
for i in items:
  log(f"Item {i}")

log(f"Hash of HASH is {hash(map(lambda x: ord(x), [*'HASH']))}")
acc = sum(map(hash, items))
print(f'Answer: {acc}')


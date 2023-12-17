from functools import reduce

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
  return list(map(int, s.strip().split()[1:]))
time = clean(input())
log("Times " + str(time))
distance = clean(input())
log("Distance " + str(distance))
races = list(zip(time, distance))
print("Races " + str(races))

# -1 or more negative speed means preparing acceleration
def possible_wins (remaining_time, remaining_distance, speed, indent):
  log(f"{indent}Possible wins of time {remaining_time}, distance {remaining_distance}, speed {speed}")
  indent = indent + " "
  new_time = remaining_time - 1
  def log2 (msg):
    log(f"{indent}{msg} at t={len(indent) - 1}, for={remaining_time}")
    return 0
  if remaining_distance <= 0:
    log(f"{indent}WIN")
    return 1
  elif remaining_time == 0:
    return 0
  elif speed <= -1:
    # Keep or release accelerator
    return \
    possible_wins(new_time, remaining_distance, speed - 1, indent) + \
    log2(f"-Release with speed {(0 - speed) - 1}") + \
    possible_wins(remaining_time, remaining_distance, (0 - speed) - 1, indent)
  else:
    # Some speed
    if (remaining_time * speed) >= remaining_distance:
      log(f"{indent}WIN")
      return 1
    else:
      return 0

result = list(map(lambda i: possible_wins(i[0], i[1], -1, ""), races))
print("Answer " + str(result))
print("Answer " + str(reduce(lambda x, y: x * y, result)))


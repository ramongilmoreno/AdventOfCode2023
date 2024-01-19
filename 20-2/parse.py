import sys
import math

from enum import Enum

def log (x, end = "\n"):
  # print(x, end = end)
  sys.stdout.flush()
  pass

print("Begin")

class Pulse(Enum):
  Low = 0
  High = 1
  def contrary (self):
    return Pulse.Low if self == Pulse.High else Pulse.High
  def __str__(self) -> str:
    # return self.name.lower()
    return str(self.value)

  def __repr__(self) -> str:
    return str(self.value)

class Module:

  def __init__ (self, name):
    self.name = name
    self.outputs = []
    self.state = Pulse.Low

  def connect_as_input_of (self, other_module):
    self.outputs.append(other_module)
    other_module.notify_new_input(self)

  def notify_new_input (self, other_module):
    pass

  def receive_pulse (self, from_module, pulse):
    if self.compute_state(from_module, pulse):
      return list((self.name, self.state, x.name) for x in self.outputs)
    else:
      return []

  # Returns True if state needs to be propagated
  def compute_state (self, from_module, pulse):
    raise_exception(f"This should not be called: {self}, {from_module}, {pulse}")

class Dummy(Module):
  def __init__ (self, name):
    super().__init__(name)
  def compute_state (self, from_module, pulse):
    return False 

class Button(Module):
  def __init__ (self):
    super().__init__('button')

  def compute_state (self, from_module, pulse):
    return True

class Broadcaster(Module):
  def __init__ (self):
    super().__init__('broadcaster')

  def compute_state (self, from_module, pulse):
    self.state = pulse
    return True

class FlipFlop(Module):
  def __init__ (self, name):
    super().__init__(name)

  def compute_state (self, from_module, pulse):
    if pulse == Pulse.Low:
      self.state = self.state.contrary()
      return True
    else:
      return False
    
class Conjunction(Module):
  def __init__ (self, name):
    super().__init__(name)
    self.inputs = {}

  def notify_new_input (self, other_module):
    self.inputs[other_module.name] = other_module.state

  def compute_state (self, from_module, pulse):
    self.inputs[from_module.name] = pulse
    self.state = Pulse.Low
    for i in self.inputs.values():
      if i == Pulse.Low:
        self.state = Pulse.High
        break
    # log(f"Computing state for {self.name}, inputs: {self.inputs}")
    return True
    
# Read configuration
modules = {}
def get_module (name):
  if not name in modules:
    return Dummy(name)
  else:
    return modules[name]
connections = []

button = Button()
modules[button.name] = button

for line in sys.stdin:
  line = line.strip()
  log(f"Line [{line}]")
  if len(line) > 0:
    elements = line.split(" ")
    source = elements[0]
    if source == "broadcaster":
      modules[source] = Broadcaster()
    else:
      source_type = source[0]
      source = source[1:]

      # Provision element
      new_element = None
      if source_type == "%":
        new_element = FlipFlop(source)
      elif source_type == "&":
        new_element = Conjunction(source)
      else:
        raise Exception(f"Unknown type {source_type} for {source}")

      modules[source] = new_element

    # Connections managed in second pass
    targets = elements[2:]
    log(f"Targets are: {targets}")
    for i in range(len(targets)):
      target = targets[i]
      if target.endswith(","):
        target = target[0:-1]
      log(f" Source {source}, target: {target}")
      connections.append((source, target))
  else:
    break

log(f"Modules {modules}")
log(f"Connections {connections}")

modules["button"].connect_as_input_of(modules["broadcaster"])
for i in connections:
  log(f"Processing connection {i}")
  get_module(i[0]).connect_as_input_of(get_module(i[1]))

# Render layout
print("")
print("https://gojs.net/latest/samples/pageFlow.html")
print("")
print('{ "class": "go.GraphLinksModel",')
print(" " + '"nodeDataArray": [')
print("  " + "{" + f'"key": "rx", "text": "rx"' + "},")
print("  " + ",".join("{" + f'"key": "{module.name}", "text": "{module.__class__.__name__}: {module.name}"' + "}" for module in modules.values()))
print(' ],')
print(' "linkDataArray": [')
print("  " + ",".join("{" + f'"from": "{connection[0]}", "to": "{connection[1]}"' + "}" for connection in connections))
print(" " + ']')
print("" + '}')
print("")

found = False
count = 0
tj = modules["tj"]
keys = tj.inputs.keys()
keys_values = {}
while not found:

  count += 1
  # Agenda is source, pulse, target
  agenda = [(button.name, Pulse.Low, "broadcaster")]
  while len(agenda) != 0:
    log(f"Agenda before: {agenda}")
    signal = agenda.pop(0)
    source = get_module(signal[0]) 
    pulse = signal[1]
    target = get_module(signal[2])

    # Find lest common multiple of pulses getting to "tj" node
    for i in keys:
      if tj.inputs[i] == Pulse.High:
        if not i in keys_values:
          keys_values[i] = count
          print(f"Found {count} for {i}, values {keys_values}")
    # print(f"{keys} and {keys_values}")
    if len(keys) == len(keys_values.values()):
      print(f'Answer (least common multiple): {math.lcm(*keys_values.values())}')
      exit(0)

    if pulse == Pulse.Low and target.name == "rx":
      print(f"Quit at count {count}")
      found = True
      agenda = []
    else:
      log(f" Signal: {source.name} -{pulse}-> {target.name}")
      agenda.extend(target.receive_pulse(source, pulse))
      log(f"  Agenda after: {agenda}")

acc = count
print(f'Answer (brute force): {acc}')


import sys
import re
from itertools import chain
from enum import Enum
from functools import cmp_to_key

# https://dev.to/turbaszek/flat-map-in-python-3g98
def flat_map(f, xs):
  ys = []
  for x in xs:
    ys.extend(f(x))
  return ys

def log (x):
  # print(x)
  pass

# Definition of enum entries
cards = list(chain(['A', 'K', 'Q', 'J', 'T'], map(str, range(9, 2 - 1, -1))))
cards_dictionary = {}
for i in cards:
  cards_dictionary[i] = 0

# Types of hands
def is_five_of_a_kind (x): return x.five_of_a_kind != None
def is_four_of_a_kind (x): return x.four_of_a_kind != None
def is_three_of_a_kind (x): return x.three_of_a_kind != None
def is_two_pair (x): return len(x.pairs) == 2
def is_single_pair (x): return len(x.pairs) == 1
def is_high_card (x): return len(x.high) == 5
def is_full_house (x): return (is_three_of_a_kind(x) and is_single_pair(x))
hand_comparison_functions = [
  is_five_of_a_kind, 
  is_four_of_a_kind, 
  is_full_house, 
  is_three_of_a_kind, 
  is_two_pair, 
  is_single_pair, 
  is_high_card
]

class Hand:
  def __init__(self, line, bet):
    self.line = line
    self.bet = bet
    self.five_of_a_kind = None
    self.four_of_a_kind = None
    self.three_of_a_kind = None
    self.pairs = []
    self.high = []
    self.dictionary = cards_dictionary.copy()
    for i in self.line:
      self.dictionary[i] += 1
      v = self.dictionary[i]
      if v == 5:
        self.five_of_a_kind = i
        self.four_of_a_kind = None
      elif v == 4:
        self.four_of_a_kind = i
        self.three_of_a_kind = None
      elif v == 3:
        self.three_of_a_kind = i
        self.pairs.remove(i)
      elif v == 2:
        self.pairs.append(i)
        self.pairs.sort(key = lambda x: cards.index(x))
        self.high.remove(i)
      elif v == 1:
        self.high.append(i)
    for i in self.dictionary:
      log(f'Dictionary {i} = {self.dictionary[i]}')
    log(f'5oak: {self.five_of_a_kind}')
    log(f'4oak: {self.four_of_a_kind}')
    log(f'3oak: {self.three_of_a_kind}')
    log(f'pairs: {self.pairs}')
    log(f'high: {self.high}')

  def __repr__(self):
    r = [ f"Hand {self.line}", f"First {self.line[0]}" ]
    for f in hand_comparison_functions:
      if f(self):
        r.append(f.__name__)
    r.append(f"Bet: {self.bet}")
    return ", ".join(r)

print("Begin")
hands = []
for line in sys.stdin:
  line = line.strip()
  elements = line.split()
  log("[" + line + "] elements " + str(elements))
  hand = Hand(elements[0], int(elements[1]))
  log(str(hand))
  hands.append(hand)

def sort_function (a, b):
  for f in hand_comparison_functions:
    va = f(a)
    vb = f(b)
    if va != vb:
      return -1 if va else 1
  
  for i in range(len(a.line)):
    r = cards.index(a.line[i]) - cards.index(b.line[i])
    if r != 0:
      return r
  return 0

hands = sorted(hands, key = cmp_to_key(sort_function), reverse = True)
log(f'Hands sorted {hands}')
acc = 0
for i in range(len(hands)):
  print(i + 1, hands[i])
  acc += ((i + 1) * hands[i].bet)
print('Answer', acc)


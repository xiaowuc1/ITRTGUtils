"""
TMC calculator

This calculator takes as inputs your DRCs/1KCs/clone count and BH+ might unlock status,
and will tell you what rebirth length maximizes the number of might levels you can
gain per second. This calculator assumes that you invest 100% of your clonetime
post might-unlock into might trainings. Consequently, you should only input the number
of clones you will devote to might trainins, as opposed to your actual clone count.

Note 1: this calculator is not tick-perfect and will likely slightly overestimate the number of
levels of might you can train in a fixed amount of time since it doesn't use ticks to ascertain
whether a level-up has been attained.

Note 2: this calculator does not offer support for recursive memory. This will remain out of
scope.
"""

class Training(object):

  def __init__(self, name, base_units, level, units_used=0):
    self.name = name
    self.level = level
    self.base_units = base_units
    self.units_used = units_used

  def needed_to_level(self):
    return (self.level+1) * self.base_units

  def level_up(self):
    self.units_used += self.needed_to_level()
    self.level += 1

print("Number of DRCs completed?")

NUM_LEVELS = int(input())
assert NUM_LEVELS >= 0 and NUM_LEVELS <= 60, "number of DRCs completed should be between 0 and 60"

print("Number of clones?")

NUM_CLONES = int(input())
assert NUM_CLONES > 0, "number of clones should be positive"

print("Number of 1KCs completed?")
ONE_KCS = int(input())
assert ONE_KCS >= 0 and ONE_KCS <= 50, "number of 1KCs completed should be between 0 and 50"

# TODO: support light clones

print("Have you unlocked the Black Hole+ Might? (Y/N)")
unlocked = input()[0] in "Yy"

RATE = 1 + 0.05 * ONE_KCS

MIGHTS = []

MIGHTS.extend([
  # base ones
  Training("HP+", base_units=1000000, level=NUM_LEVELS),
  Training("Att+", base_units=1000000, level=NUM_LEVELS),
  Training("Def+", base_units=1000000, level=NUM_LEVELS),
  Training("Regen+", base_units=1000000, level=NUM_LEVELS),
  Training("Battle+", base_units=1000000, level=NUM_LEVELS),
  Training("CoD+", base_units=1000000, level=NUM_LEVELS),
  Training("CoP+", base_units=1000000, level=NUM_LEVELS),
  Training("PS+", base_units=1000000, level=NUM_LEVELS),
])

if unlocked:
  # BH might proxy
  MIGHTS.append(Training("BH+", base_units=1000000, level=NUM_LEVELS))

MIGHTS.extend([
  # unleashes
  Training("FB+", base_units=500000, level=NUM_LEVELS),
  Training("DA+", base_units=750000, level=NUM_LEVELS),
  Training("OA+", base_units=1000000, level=NUM_LEVELS),
  Training("EM+", base_units=1500000, level=NUM_LEVELS),
  Training("MM+", base_units=2000000, level=NUM_LEVELS),
  Training("TA+", base_units=2500000, level=NUM_LEVELS),
])

levels_gained = [NUM_LEVELS] * len(MIGHTS)
curr_time = 94.5 * 60
best_might_rate = (sum(levels_gained) / curr_time)
while True:
  best_index = 0
  for i in range(len(MIGHTS)):
    if MIGHTS[i].needed_to_level() < MIGHTS[best_index].needed_to_level():
      best_index = i
  secs_needed = MIGHTS[best_index].needed_to_level() / float(RATE * NUM_CLONES)
  new_might_rate = (sum(levels_gained) + 1) / (curr_time + secs_needed)
  if new_might_rate < best_might_rate:
    break
  best_might_rate = new_might_rate
  MIGHTS[best_index].level_up()
  levels_gained[best_index] += 1
  curr_time += secs_needed
  print("{} levels in {} seconds for {} levels per second".format(sum(levels_gained), curr_time, best_might_rate))

for might in MIGHTS:
  print("train {} to {}".format(might.name, might.level))

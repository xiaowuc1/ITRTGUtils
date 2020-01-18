"""
DMC calculator

This calculator takes as inputs your DRCs/CBCs/1KCs/clone count and BH+ might unlock status,
along with the number of runs of a fixed length that you wish to complete, and will tell you
the optimal number of might levels to train for a run of that length. Most people will
probably do between 10-15 runs.

This calculator assumes that you invest 100% of your clonetime post-might unlock into might
trainings. Consequently, you should only input the number of clones you will devote to might
trainins, as opposed to your actual clone count.

Note 1: this calculator is not tick-perfect and will likely slightly overestimate the number of
levels of might you can train in a fixed amount of time since it doesn't use ticks to ascertain
whether a level-up has been attained.

Note 2: this calculator does not offer support for recursive memory. This will remain out of
scope.
"""

class Training(object):

  def __init__(self, name, base_units, level, ghost_levels):
    self.name = name
    self.level = level
    self.base_units = base_units
    self.ghost_levels = ghost_levels

  def needed_to_level(self):
    return (self.level+1) * self.base_units

  def level_up(self):
    self.level += 1

print("Number of DRCs completed?")

DRCS = int(input())
assert DRCS >= 0 and DRCS <= 60, "number of DRCs completed should be between 0 and 60"

print("Number of CBCs completed?")

CBCS = int(input())
assert CBCS >= 0 and CBCS <= 60, "number of CBCs completed should be between 0 and 60"

print("Number of clones?")

NUM_CLONES = int(input())
assert NUM_CLONES > 0, "number of clones should be positive"

print("Number of 1KCs completed?")
ONE_KCS = int(input())
assert ONE_KCS >= 0 and ONE_KCS <= 50, "number of 1KCs completed should be between 0 and 50"

RATE = 1 + 0.05 * ONE_KCS

# TODO: support light clones

print("Have you unlocked the Black Hole+ Might? (Y/N)")
unlocked = input()[0] in "Yy"

MIGHTS = []

MIGHTS.extend([
  # base ones
  Training("HP+", base_units=1000000, level=DRCS, ghost_levels=CBCS),
  Training("Att+", base_units=1000000, level=DRCS, ghost_levels=CBCS),
  Training("Def+", base_units=1000000, level=DRCS, ghost_levels=CBCS),
  Training("Regen+", base_units=1000000, level=DRCS, ghost_levels=CBCS),
  Training("Battle+", base_units=1000000, level=DRCS, ghost_levels=CBCS),
  Training("CoD+", base_units=1000000, level=DRCS, ghost_levels=CBCS),
  Training("CoP+", base_units=1000000, level=DRCS, ghost_levels=CBCS),
  Training("PS+", base_units=1000000, level=DRCS, ghost_levels=CBCS),
])

if unlocked:
  # BH might proxy
  MIGHTS.append(Training("BH+", base_units=1000000, level=DRCS, ghost_levels=CBCS))

MIGHTS.extend([
  # unleashes
  Training("FB+", base_units=500000, level=DRCS, ghost_levels=CBCS),
  Training("DA+", base_units=750000, level=DRCS, ghost_levels=CBCS),
  Training("OA+", base_units=1000000, level=DRCS, ghost_levels=CBCS),
  Training("EM+", base_units=1500000, level=DRCS, ghost_levels=CBCS),
  Training("MM+", base_units=2000000, level=DRCS, ghost_levels=CBCS),
  Training("TA+", base_units=2500000, level=DRCS, ghost_levels=CBCS),
])

print("Number of runs:")
runs = int(input())
assert runs >= 1 and runs <= 15, "the number of runs must be between 1 and 15"
secs = (3600 * 24. / runs) - 189 * 30
print(secs)
while secs > 0:
  best_index = 0
  for i in range(len(MIGHTS)):
    if MIGHTS[i].needed_to_level() < MIGHTS[best_index].needed_to_level():
      best_index = i
      # do some tick rubber_banding
      # TODO: revert to reverse engineering ticks?
      if 1 / MIGHTS[i].needed_to_level() <= 33:
        break
  secs_needed = max(1/33.34, MIGHTS[best_index].needed_to_level() / float(RATE * NUM_CLONES))
  if secs_needed > secs:
    break
  secs -= secs_needed
  MIGHTS[best_index].level_up()

total_gain = 0
for might in MIGHTS:
  total_gain += might.level + might.ghost_levels

print("gain {} levels, {} total".format(total_gain, total_gain * runs))
for might in MIGHTS:
  print("train {} to {}".format(might.name, might.level))

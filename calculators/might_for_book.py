from math import log10, sqrt

class Training(object):

  def __init__(self, name, level, base_units, factor, ghost_levels):
    self.name = name
    self.level = level
    self.base_units = base_units
    self.factor = factor
    self.ghost_levels = ghost_levels

  def needed_to_level(self):
    return (self.level+1) * self.base_units

  def level_up(self):
    self.level += 1

  def get_bonus(self, dmc_bonus):
    return 1 + (1+dmc_bonus*(self.level+self.ghost_levels)) * self.factor

  def get_log_bonus(self, dmc_bonus):
    return log10(self.get_bonus(dmc_bonus))

  def get_increment(self, dmc_bonus):
    self.level += 1
    new_gain = self.get_log_bonus(dmc_bonus)
    self.level -= 1
    return new_gain - self.get_log_bonus(dmc_bonus)

print("Number of DRCs completed?")
DRCS = int(input())
assert DRCS >= 0 and DRCS <= 60, "number of DRCs completed should be between 0 and 60"
print("Number of CBCs completed?")
CBCS = int(input())
assert CBCS >= 0 and CBCS <= 60, "number of CBCs completed should be between 0 and 60"
print("DMC score?")
DMC = int(input())
assert 0 < DMC <= 250000, "DMC score must be positive and <= 250000"

dmc_bonus = sqrt(DMC) / 500 / 100

MIGHTS = [
  # unleashes
  Training(name="OA+", level=DRCS, base_units=1000000, factor=1, ghost_levels=CBCS),
  Training(name="EM+", level=DRCS, base_units=1500000, factor=1, ghost_levels=CBCS),
  Training(name="MM+", level=DRCS, base_units=2000000, factor=1.5, ghost_levels=CBCS),
  Training(name="TA+", level=DRCS, base_units=2500000, factor=2, ghost_levels=CBCS),
]

print("Multiplicative factor? (must be integral)")
GOAL = int(input())
assert GOAL > 1, "must be a positive integer greater than 1"

LOG_GOAL = log10(GOAL)

while True:
  current_bonus = 0
  real_bonus = 1
  for i in range(4):
    current_bonus += MIGHTS[i].get_log_bonus(dmc_bonus)
    real_bonus *= MIGHTS[i].get_bonus(dmc_bonus)
  if current_bonus >= LOG_GOAL:
    break
  fastest_improvement = 0
  best_idx = -1
  for i in range(4):
    improvement = MIGHTS[i].get_increment(dmc_bonus) / MIGHTS[i].needed_to_level()
    if improvement > fastest_improvement:
      best_idx = i
      fastest_improvement = improvement
  MIGHTS[best_idx].level_up()

for i in range(4):
  print("train {} to {}".format(MIGHTS[i].name, MIGHTS[i].level))

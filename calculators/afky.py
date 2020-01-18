"""
afky calculator

This calculator will compute, given a fixed clone count in afky, the optimal
amount of HP for that clone count.
"""

from math import ceil

def solve(cloneCount):
  lhs = 1
  # TODO: do O(log ans) ternary search instead of assuming a large value
  rhs = 10 ** 100
  while lhs < rhs:
    hp = (lhs+rhs+1)//2
    x = hp
    y = cloneCount
    lhsBonus = ((x+1)**1.1) * (y**0.9) - (x**1.1)*(y**0.9)
    lhsBonus /= (x*x*100/3 + ((x+1)*y-1)*(x+1)*y/2.-(x*y-1)*(x*y)/2.)
    rhsBonus = ((x)**1.1) * ((y+1)**0.9) - (x**1.1)*(y**0.9)
    rhsBonus /= (y*y*100 + (x*(y+1)-1)*x*(y+1)/2.-(x*y-1)*(x*y)/2.)
    if lhsBonus > rhsBonus:
      lhs = hp
    else:
      rhs = hp-1
    return lhs

print("Desired clone count:")
v = int(input())
amt = solve(v)
print("HP should be {}, power of {}".format(amt, v*amt))

#!/usr/bin/env python3 
# vim: nospell:sta:et:sw=2:ts=2:sts=2
"""
Divide numbers.
"""

import math
from   lib   import THE,Pretty,same,first,last,ordered
from   copy  import deepcopy as kopy
from   thing import Num,Sym

class Div2(Pretty):
  """
  Recursively divide a list of numns by finding splits
  that minimizing the expected value of the standard
  deviation (after the splits).
  """
  def __init__(i,lst, x=first, y=last, xis=Num, yis=Num):
    i.xis    = xis
    i.yis    = yis

    # i._lst   = sorted(firstx)
    # i._lsty   = sorted(lasty)

    i._lst   = ordered(lst, key=x)
    i._lsty   = ordered(lst, key=y)

    i.b4     = i.xis(i._lst,key=x)
    i.b4y     = i.yis(i._lsty,key=y)

    i.gain   = 0                             # where we will be, once done
    i.x      = x                             # how to get values from 'lst' items
    i.y      = y
    i.step   = int(len(i._lst)**THE.div.min) # each split need >= 'step' items
   
    # start stop
    i.stop   = x(last(i._lst))               # top list value
    i.start  = x(first(i._lst))              # bottom list value
    i.stopy   = x(last(i._lsty))               # top list value
    i.starty  = x(first(i._lsty))
    
    i.ranges = []                            # the generted ranges
    i.epsilon= i.b4.sd() * THE.div.cohen     # bins must be seperated >= epsilon
    i.__divide(1, len(i._lst), i.b4, 1, len(i._lsty), i.b4y, 1)

    i.gain   /= len(i._lst)

  def __divide(i, lo, hi, b4, loy, hiy, b4y, rank):
    "Find a split between lo and hi, then recurse on each split."
    xl    = i.xis(key=i.x)
    yl    = i.yis(key=i.x)
    
    xr    = i.xis(key=i.y)
    yr    = i.yis(key=i.y)
    

    cutxl    = Num()
    cutyl    = Num()
    
    cutxr    = Num()
    cutyr    = Num()

    best = i.b4y.variety()
    cut  = None
    cutLocation = -1
    #  start stop
    for j in range(loy, hiy):

      yl + i._lsty[j]
      yr - i._lsty[j]

      if yl.n >= i.step:
        if yr.n >= i.step:
          now   = i.y( i._lsty[j-1] ) 
          after = i.y( i._lsty[j] ) 
          if now == after: continue
          if abs(yr.mu - yl.mu) >= i.epsilon:
            if after - i.start >= i.epsilon:
              if i.stop - now >= i.epsilon: 
                xpect = yl.xpect(r)
                if xpect*THE.div.trivial < best:
                  best, cut = xpect, j
                  cutLocation = j
                  cutxl = Num(xl)
                  cutxr = Num(xr)
                  cutyl = Num(yl)
                  cutyr = Num(yr)
    if cut:
      # ls, rs = i._lsty[lo:cut], i._lsty[cut:hi] 
      rank   = i.__divide2(cutxl, cutyl, rank) + 1
      rank   = i.__divide2(cutxr, cutyr, rank)
    else:
      i.gain   += b4y.n * b4y.variety()
      b4y.rank   = rank
      i.ranges += [ b4y ]
    return rank




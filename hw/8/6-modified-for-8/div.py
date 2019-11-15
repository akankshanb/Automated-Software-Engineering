#!/usr/bin/env python3 
# vim: nospell:sta:et:sw=2:ts=2:sts=2
"""
Divide numbers.
"""

import math
from   lib   import THE,Pretty,same,first,last,ordered
from   copy  import deepcopy as kopy
from   thing import Num,Sym

class Div(Pretty):
  """
  Recursively divide a list of numns by finding splits
  that minimizing the expected value of the standard
  deviation (after the splits).
  """
  def __init__(i,lst, x=same,xis=Num):
    i.xis    = xis
    i._lst   = ordered(lst,key=x)
    i.b4     = i.xis(i._lst,key=x)
    # print("hi", i.b4)
    i.gain   = 0                             # where we will be, once done
    i.x      = x                             # how to get values from 'lst' items
    i.step   = int(len(i._lst)**THE.div.min) # each split need >= 'step' items
    i.stop   = x(last(i._lst))               # top list value
    i.start  = x(first(i._lst))              # bottom list value
    i.ranges = []                            # the generted ranges
    i.epsilon= i.b4.sd() * THE.div.cohen     # bins must be seperated >= epsilon
    i.__divide(1, len(i._lst), i.b4, 1)
    i.gain   /= len(i._lst)

  def __divide(i, lo, hi, b4, rank):
    "Find a split between lo and hi, then recurse on each split."
    l    = i.xis(key=i.x)
    r    = i.xis(i._lst[lo:hi], key=i.x)
    best = b4.variety()
    cut  = None
    for j in range(lo,hi):
      l + i._lst[j]
      r - i._lst[j]
      if l.n >= i.step:
        if r.n >= i.step:
          now   = i.x( i._lst[j-1] ) 
          after = i.x( i._lst[j] ) 
          if now == after: continue
          if abs(r.mu - l.mu) >= i.epsilon:
            if after - i.start >= i.epsilon:
              if i.stop - now >= i.epsilon: 
                xpect = l.xpect(r)
                if xpect*THE.div.trivial < best:
                  best, cut = xpect, j
    if cut:
      ls, rs = i._lst[lo:cut], i._lst[cut:hi] 
      rank   = i.__divide(lo, cut, i.xis(ls,key=i.x), rank) + 1
      rank   = i.__divide(cut ,hi, i.xis(rs,key=i.x), rank)
    else:
      i.gain   += b4.n * b4.variety()
      b4.rank   = rank
      i.ranges += [ b4 ]
    return rank

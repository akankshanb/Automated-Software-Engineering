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

  def __init__(i, lst, x=first, xis=Num, y=last, yis=Num):
    i.x, i.xis = x, xis
    i.y, i.yis = y, yis
    # print("LIST: ", lst)
    # print("LIST: ", i.y, i.yis)
    # i._lst     = list(map(lambda x: x.cells, lst))
    # i._lst     = ordered(lst,key=x)
    i._lst = lst # we need this or row tobe ordered
    i._lst.sort(key = lambda test_list: test_list.cells[0]) 

    # print("LIST: ", i._lst)
    i.xs       = i.xis(i._lst,key=x)
    i.ys       = i.yis(i._lst,key=y)
    i.gain     = 0                             # where we will be, once done
    i.step     = int(len(i._lst)**THE.div.min) # each split need >= 'step' items
    i.stop     = x(last(i._lst))               # top list value
    i.start    = x(first(i._lst))              # bottom list value
    i.ranges   = []                            # the generted ranges
    i.epsilon  = i.xs.sd() * THE.div.cohen     # bins must be seperated >= epsilon
    i.finalcut = 0
    i.finallow = 0

    i.__divide(1, len(i._lst), i.xs, i.ys, 1)

    
  def finalcutlow(i):
    return i.finalcut, i.finallow

  def __divide(i, lo, hi, xr, yr, rank):
    "Find a split between lo and hi, then recurse on each split."
    xb4       = kopy(xr)
    xb4.stats = kopy(yr)
    xl        = i.xis(key=i.x)
    yl        = i.yis(key=i.y)
    best      = yr.variety()
    cut       = None
    # print("xl: ", xl)
    # print("yl: ", yl)
    for j in range(lo,hi):
      xl + i._lst[j]
      yl + i._lst[j]
      xr - i._lst[j]
      yr - i._lst[j]
      if xl.n >= i.step:
        if xr.n >= i.step:
          # if j == 391:
            # print("list: ", i._lst[j])

          now   = i.x( i._lst[j]   )
          if j+1 < len(i._lst):
            after = i.x( i._lst[j+1] )
          else:
            # print("HERE: ",  i._lst[j])
            after = i.x( i._lst[j] )
          if now == after: continue
          if abs(xr.mu - xl.mu) >= i.epsilon:
            if after - i.start >= i.epsilon:
              if i.stop - now >= i.epsilon:
                xpect = yl.xpect(yr)
                if xpect*THE.div.trivial < best:
                  best, cut = xpect, j
    if cut:
      ls, rs = i._lst[lo:cut], i._lst[cut:hi]
      i.finalcut = cut
      i.finallow = lo
      rank   = i.__divide(lo, cut, i.xis(ls, key=i.x), i.yis(ls, key=i.y), rank) + 1
      rank   = i.__divide(cut, hi, i.xis(rs, key=i.x), i.yis(rs, key=i.y), rank)
    else:
      xb4.rank  = rank
      i.ranges += [ xb4 ]
    return rank
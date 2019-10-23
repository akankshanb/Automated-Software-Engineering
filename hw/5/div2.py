"""
Divide numbers.
"""

import math
from   lib   import THE,Pretty,same,first,last,ordered
from   copy  import deepcopy as kopy
from thing import Num,Sym
# from Sym import Sym

class Div2(Pretty):
  """
  Recursively divide a list of numns by finding splits
  that minimizing the expected value of the standard
  deviation (after the splits).
  """
  def __init__(i,lst, x = "first", y = "last", yis="Num"):
    i.yis    = yis
    i.x_lst, i.y_lst = i.createXYList(lst, yis)
    i.b4     = i.y_lst
    i._lst   = i.y_lst.numList if i.yis == "Num" else i.y_lst.symList
    i.gain   = 0                             # where we will be, once done
    i.step   = int(i.y_lst.n**THE.div.min) # each split need >= 'step' items
    i.stop   = last(i.y_lst.numList) if i.yis == "Num" else last(i.y_lst.symList)         # top list value
    i.start  = first(i.y_lst.numList) if i.yis == "Num" else first(i.y_lst.symList)          # bottom list value
    i.ranges = []                            # the generted ranges
    i.epsilon= i.y_lst.variety() * THE.div.cohen     # bins must be seperated >= epsilon
    i.__divide(0, i.b4.n, i.b4, 1)
    i.gain   /= len(i._lst)
    i.splitXList()

  def createXYList(i, lst, yis):
    lst = sorted(lst, key = lambda x: x[1])
    x_lst = Num()
    if yis == "Num":
      y_lst = Num()
    else:
      y_lst = Sym()
    for i in lst:
      x_lst.add(i[0])
      y_lst.add(i[1])

    return x_lst, y_lst

  def numSplit(i, lst):
    newNumber = Num()
    if lst:
      for x in lst:
        newNumber.add(x)
    return newNumber

  def symSplit(i, lst):
    newSymbol = Sym()
    if lst:
      for x in lst:
        newSymbol.add(x)
    return newSymbol

  def splitXList(i):
    start = 0
    i.xranges = []
    for j in i.ranges:
      i.xranges.append(i.numSplit(i.x_lst.numList[start:start+j.n]))
      start += j.n

  def __divide(i, lo, hi, b4, rank):
    "Find a split between lo and hi, then recurse on each split."

    if i.yis == "Num":
      l    = i.numSplit([])
      r    = i.numSplit(i._lst[lo:hi])
      i.stop  = last(b4.numList)              
      i.start = first(b4.numList) 
    else:
      l    = i.symSplit([])
      r    = i.symSplit(i._lst[lo:hi])
      i.stop   = last(b4.symList)              
      i.start  = first(b4.symList) 

    i.epsilon = b4.variety() * THE.div.cohen
    best = b4.variety()
    cut  = None
    for j in range(lo,hi):
      l.add(i._lst[j])
      r.sub(i._lst[j])
    
      if l.n >= i.step:
        if r.n >= i.step:
          now   = i._lst[j-1]
          after = i._lst[j] 
          if now == after: continue
          if i.yis == "Num":
            if abs(r.mu - l.mu) >= i.epsilon:
              if after - i.start >= i.epsilon:
                if i.stop - now >= i.epsilon: 
                  xpect = l.xpect(r)
                  if xpect*THE.div.trivial < best:
                    best, cut = xpect, j
          else:
            if abs(ord(r.mode) - ord(l.mode)) >= i.epsilon:
              if ord(after) - ord(i.start) >= i.epsilon:
                if ord(i.stop) - ord(now) >= i.epsilon: 
                  xpect = l.xpect(r)
                  if xpect*THE.div.trivial < best:
                    best, cut = xpect, j

    if cut:
      ls, rs = i._lst[lo:cut], i._lst[cut:hi] 
      if i.yis == "Num":
        rank   = i.__divide(lo, cut, i.numSplit(ls), rank) + 1
        rank   = i.__divide(cut ,hi, i.numSplit(rs), rank)
      else:
        rank   = i.__divide(lo, cut, i.symSplit(ls), rank) + 1
        rank   = i.__divide(cut ,hi, i.symSplit(rs), rank)
    else:
      i.gain   += b4.n * b4.variety()
      i.ranges += [b4]
    return rank

  def printValues(i):
    if i.yis == "Num":
      print("Output for data 1:")
      for k in range(len(i.ranges)):
        numX = i.xranges[k]
        numY = i.ranges[k]
        print(str(k+1) + " x.n\t" + str(numX.n) + " | x.lo " + str(round(numX.lo,4)) + " | x.hi " + str(round(numX.hi,4)) + " | y.lo " + str(round(numY.lo,4)) + " | y.hi " + str(round(numY.hi,4)))
    else:
      print("Output for data 2:")
      for k in range(len(i.ranges)):
        symX = i.xranges[k]
        symY = i.ranges[k]
        print(str(k+1) + " x.n\t" + str(symX.n) + " | x.lo " + str(round(symX.lo,4)) + " | x.hi " + str(round(symX.hi,4)) + " | y.mode " + str(symY.mode) + " | y.ent " + str(round(symY.variety(),4)))
    
    print()
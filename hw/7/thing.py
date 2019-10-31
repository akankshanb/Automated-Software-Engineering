#!/usr/bin/env python3
# vim: sta:et:sw=2:ts=2:sts=2
"""
Keep knowledge about Num or Sym columns.
"""

from  lib   import *
import math
import operator
# from div2 import Div2

class Thing(Pretty):
  "Abstract class for Nums and Syms"

  def xpect(i,j):
    n = i.n + j.n
    return i.n/n*i.variety() + j.n/n*j.variety()

  def __add__(i,x):
    # print("add here")
    y = i.key(x)
    if y != THE.char.skip:
      i.n += 1
      i.add(y)
    return x

  def __sub__(i,x):
    # print("sub here")
    y = i.key(x)
    if y != THE.char.skip:
      i.n -= 1
      i.sub(y)
    return x

class Num(Thing):
  "Track numbers seen in a column"
  def __init__(i, inits=[], pos=0,txt="",w=1,key=same):
    i.pos, i.txt   = pos, txt
    i.key          = key 
    i.rank, i.like = 1,1
    i.n, i.w       = 0, w
    i.mu, i.m2     = 0, 0
    i.lo, i.hi     = 10 ** 32, -10 ** 32
    # i.count = 0
    i.numList = []
    i.inits = []
    # [i + x for x in inits]
    

  def variety(i): 
    return i.sd()

  def sd(i):
    if i.n  < 2: return 0
    if i.m2 < 0: return 0
    return  (i.m2 / (i.n - 1 + 10**-32)) ** 0.5

  def add(i, x):
      # i.numList.append(x)
      i.inits.append(x)
      i.n += 1
      if x < i.lo: i.lo = x
      if x > i.hi: i.hi = x
      d = x - i.mu
      if not i.n == 0:
        i.mu += d / i.n
      i.m2 += d * (x - i.mu)

  def sub(i, x):
      # i.numList.remove(x)
      i.inits.remove(x)
      i.n -= 1
      if i.n < 2:
        i.n, i.mu, i.m2 = 0, 0, 0
      else:
        d = x - i.mu
        i.mu -= d / i.n
        i.m2 -= d * (x - i.mu)

  # "i" is a Num instance, "x" and "y" are numbers, "no=?".
  def dist(i,x,y):
    norm = lambda z: (z - i.lo)/(i.hi - i.lo + 10**-32)
    # print("x num: ", i.lo)
    # print("x den: ", i.hi)
    no = THE.char.skip
    if x is no:
      if y is no: return 1
      y = norm(y)
      x = 0 if y > .5 else  1
    else:
      x = norm(x) 
      # print("x: ", x)
      if y is no:
          y = 0 if x > .5 else  1
      else:
          y = norm(y)
          # print("y: ", y)
    # print("x: ", x)
    # print("y: ", y)
    return abs(x-y)

  def cos(i,x,y,z,c):
    return (i.dist(x,z)**2 + c**2 - i.dist(y,z)**2)/(2*c) 

class Sym(Thing):
  def __init__(i,inits=[],pos=0,txt="",w=1,key=same):
    i.pos, i.txt = pos, txt
    i.n, i.w       = 0, w
    i.key          = key 
    i.rank, i.like = 1,1
    i.mode         = None
    i.most         = 0
    i.cnt          = {}
    # i.count = 0
    i.symList = []
    # [i + x for x in inits]

  def add(i,x):
    i.symList.append(x)
    i.n += 1
    new = i.cnt.get(x,0) + 1
    i.cnt[x] = new
    if new > i.most:
      i.mode, i.most = x,new

  def sub(i,x):
    i.symList.remove(x)
    i.cnt[x] -= 1
    i.n -= 1
    old = i.cnt.get(x,0)
    if old > 0:
      i.cnt[x] = old - 1
    if i.cnt:
      i.mode = max(i.cnt.items(), key=operator.itemgetter(1))[0]
      i.most = i.cnt[i.mode]
      
  def variety(i): 
    return i.ent()

  def ent(i):
    e=0
    for v in i.cnt.values():
      if v > 0 and not i.n == 0: 
        p = v/i.n
        e += -1*p*math.log(p,2)
    return e

  # "i" is a Sym instance, "x" and "y" and symols, "n=?"
  def dist(i,x,y):
    # print("sym num: ")
    no = THE.char.skip
    if x is no and y is no: return 1
    if x != y : return 1
    return 0

  def cos(i,x,y,z,c):
    return (i.dist(x,z)**2 + c**2 - i.dist(y,z)**2)/(2*c)

